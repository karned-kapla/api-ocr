from models.ocr_model import OcrCreate, OcrRead, OcrUpdate
from services.ocr_service import OcrService

ocr_service = OcrService()

def service_create_ocr(request, ocr: OcrCreate) -> str:
    return ocr_service.create_ocr(request, ocr)

def service_read_ocr(request, uuid: str) -> OcrRead:
    return ocr_service.read_ocr(request, uuid)

def service_update_ocr(request, ocr_update: OcrUpdate) -> None:
    ocr_service.update_ocr(request, ocr_update)

def service_delete_ocr(request, uuid: str) -> None:
    ocr_service.delete_ocr(request, uuid)
