from abc import ABC, abstractmethod
from models.ocr_model import OcrCreate, OcrUpdate

class OcrRepository(ABC):

    @abstractmethod
    def create_ocr(self, ocr_create: OcrCreate):
        pass

    @abstractmethod
    def read_ocr(self, ocr_id: str):
        pass

    @abstractmethod
    def update_ocr(self, ocr_id: str, ocr_update: OcrUpdate):
        pass

    @abstractmethod
    def delete_ocr(self, ocr_id: str):
        pass

    @abstractmethod
    def close(self):
        pass