from fastapi import HTTPException
from common_api.middlewares.v1.database_middleware import check_repo
from common_api.utils.v0 import get_state_repos
from common_api.services.v0 import Logger
from config import KAFKA_TOPIC, MS_SECRET_TTL
from models.ocr_model import OcrCreate, OcrCreateDatabase, OcrRead, OcrUpdate
from repositories import get_repositories
from services.cache_service import CacheService
from services.message_service import MessageService
from services.secret_service import SecretService

logger = Logger()

class OcrService:
    def __init__(self):
        self.cache_service = CacheService()
        self.message_service = MessageService()
    
    def create_ocr(self, request, ocr: OcrCreate) -> str:
        try:
            repos = get_state_repos(request)

            ocr_db = OcrCreateDatabase(**ocr.model_dump())
            ocr_db.status = "pending"
            ocr_db.secret = SecretService.generate_secret()
            ocr_db.created_by = request.state.token_info.get('user_uuid')

            ocr_uuid = repos.ocr_repo.create_ocr(ocr_db)
            
            if not isinstance(ocr_uuid, str):
                raise TypeError("The method create_ocr did not return a str.")

            credential = self.cache_service.get_database_credential(request.state.licence_uuid)

            payload = {
                "credential": credential,
                "licence_uuid": request.state.licence_uuid,
                "entity_uuid": request.state.entity_uuid
            }
            self.cache_service.store_context(ocr_db.secret, payload, MS_SECRET_TTL)

            self.message_service.send_ocr_task(
                topic=KAFKA_TOPIC,
                ocr_uuid=ocr_uuid,
                secret=ocr_db.secret,
                url=ocr_db.url,
                model=ocr_db.model
            )
            
            return ocr_uuid
        except Exception as e:
            logger.error(f"Error creating ocr: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while creating the ocr: {e}")
    
    def read_ocr(self, request, uuid: str) -> OcrRead:
        try:
            repos = get_state_repos(request)
            ocr = repos.ocr_repo.read_ocr(uuid)
        except Exception as e:
            logger.error(f"Error reading ocr: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the ocr: {e}")
        
        if ocr is None:
            raise HTTPException(status_code=404, detail="Ocr not found")
        
        return ocr
    
    def update_ocr(self, request, ocr_update: OcrUpdate) -> None:
        try:
            try:
                payload = self.cache_service.get_context(ocr_update.secret)
                credential = payload["credential"]
            except ValueError as e:
                logger.error(f"Error getting context: {e}")
                raise HTTPException(status_code=403, detail="Invalid or expired secret")

            repos = get_repositories(uri=credential['uri'])
            check_repo(repos)

            setattr(request.state, 'licence_uuid', payload['licence_uuid'])
            setattr(request.state, 'entity_uuid', payload['entity_uuid'])
            setattr(request.state, 'repos', repos)

            existing_ocr = repos.ocr_repo.read_ocr(ocr_update.uuid)
            
            if not existing_ocr:
                raise HTTPException(status_code=404, detail="Ocr not found")

            if not SecretService.validate_secret(existing_ocr.get('secret'), ocr_update.secret):
                if existing_ocr.get('secret') is None or existing_ocr.get('secret') == "":
                    raise HTTPException(status_code=403, detail="Secret is required for update")
                else:
                    raise HTTPException(status_code=403, detail="Invalid secret")

            update_data = OcrUpdate(
                uuid=ocr_update.uuid,
                secret="",
                status="completed",
                model=ocr_update.model,
                result=ocr_update.result
            )

            repos.ocr_repo.update_ocr(ocr_update.uuid, update_data)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating ocr: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the ocr: {e}")
    
    def delete_ocr(self, request, uuid: str) -> None:
        try:
            repos = get_state_repos(request)
            repos.ocr_repo.delete_ocr(uuid)
        except Exception as e:
            logger.error(f"Error deleting ocr: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while deleting the ocr: {e}")