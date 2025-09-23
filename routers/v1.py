from fastapi import APIRouter, HTTPException, status, Request
from config.config import API_TAG_NAME
from common_api.decorators.v0.check_permission import check_permissions
from models.ocr_model import OcrCreate, OcrRead, OcrUpdate, OcrCreateDatabase
from common_api.services.v0 import Logger
from services.ocrs_service import service_create_ocr, service_read_ocr, service_update_ocr, service_delete_ocr

logger = Logger()

VERSION = "v1"
api_group_name = f"/{API_TAG_NAME}/{VERSION}/"

router = APIRouter(
    tags=[api_group_name],
    prefix=f"/ocr/{VERSION}"
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@check_permissions(['create'])
async def router_create_ocr(request: Request, ocr: OcrCreate) -> dict:
    logger.api("POST /ocr/v1/")
    new_uuid = service_create_ocr(request, ocr)
    return {"uuid": new_uuid}


@router.get("/{uuid}", status_code=status.HTTP_200_OK, response_model=OcrRead)
@check_permissions(['read', 'read_own'])
async def router_read_ocr(request: Request, uuid: str):
    logger.api("GET /ocr/v1/{uuid}")
    ocr = service_read_ocr(request, uuid)
    if ocr is None:
        raise HTTPException(status_code=404, detail="Ocr not found")
    return ocr


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
@check_permissions(['delete', 'delete_own'])
async def router_delete_ocr(request: Request, uuid: str):
    logger.api("DELETE /ocr/v1/{uuid}")
    service_delete_ocr(request, uuid)


@router.put("/tasks/results", status_code=status.HTTP_204_NO_CONTENT)
async def router_update_ocr(request: Request, ocr_update: OcrUpdate):
    logger.api("PUT /ocr/v1/tasks/results")
    service_update_ocr(request, ocr_update)
