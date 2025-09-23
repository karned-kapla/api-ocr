from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any


class OcrBase(BaseModel):
    url: HttpUrl
    model: Optional[str] = None


class OcrCreate(OcrBase):
    pass


class OcrCreateDatabase(OcrBase):
    status: str = "pending"
    secret: str = None
    created_by: Optional[str] = Field(None, description="User who created the ocr")


class OcrRead(OcrBase):
    uuid: str
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    created_by: Optional[str] = Field(None, description="User who created the ocr")


class OcrUpdate(BaseModel):
    uuid: str
    secret: str
    status: Optional[str] = None
    model: str
    result: Optional[Dict[str, Any]] = None
