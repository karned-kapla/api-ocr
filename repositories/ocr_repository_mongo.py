import re
from urllib.parse import urlparse
from uuid import uuid4

from pymongo import MongoClient

from interfaces.ocr_interface import OcrRepository
from models.ocr_model import OcrCreateDatabase, OcrUpdate
from schemas.ocr_schema import ocr_serial

def check_uri(uri):
    if not re.match(r"^mongodb://", uri):
        raise ValueError("Invalid URI: URI must start with 'mongodb://'")


def extract_database(uri: str) -> str:
    parsed_uri = urlparse(uri)
    db_name = parsed_uri.path.lstrip("/")

    if not db_name:
        raise ValueError("L'URI MongoDB ne contient pas de nom de base de données.")

    return db_name


class OcrRepositoryMongo(OcrRepository):

    def __init__(self, uri):
        check_uri(uri)
        database = extract_database(uri)

        self.uri = uri
        self.client = MongoClient(self.uri)
        self.db = self.client[database]
        self.collection = "ocrs"

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def create_ocr(self, ocr_create: OcrCreateDatabase) -> str:
        ocr_data = ocr_create.model_dump()
        if "url" in ocr_data and ocr_data["url"] is not None:
            ocr_data["url"] = str(ocr_data["url"])
        ocr_id = str(uuid4())
        ocr_data["_id"] = ocr_id
        try:
            new_uuid = self.db[self.collection].insert_one(ocr_data)
            return new_uuid.inserted_id
        except Exception as e:
            raise ValueError(f"Failed to create ocr in database: {str(e)}")

    def read_ocr(self, uuid: str) -> dict:
        result = self.db[self.collection].find_one({"_id": uuid})
        if result is None:
            return {}
        ocr = ocr_serial(result)
        return ocr

    def update_ocr(self, uuid: str, ocr_update: OcrUpdate) -> None:
        update_fields = ocr_update.model_dump()
        update_fields.pop('created_by', None)
        update_fields.pop('uuid', None)
        update_data = {"$set": update_fields}
        self.db[self.collection].find_one_and_update({"_id": uuid}, update_data)


    def delete_ocr(self, uuid: str) -> None:
        self.db[self.collection].delete_one({"_id": uuid})

    def close(self):
        self.client.close()
