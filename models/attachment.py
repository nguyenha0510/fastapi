
from beanie import Document
from pydantic import BaseModel
from typing import Optional, Any


class Attachment(Document):
    parent_id: str
    file_name: str
    file_size: str
    author: str
    url: str

    class Collection:
        name = "attachment"

    class Config:
        orm_mode = True,
        schema_extra = {
            "example": {
                "parent_id": "7fgh8ew7f8sdh7cew7",
                "file_name": "Tai lieu",
                "file_size": "30Mb",
                "author": "78yc8h348df23h89dh2",
            }
        }


class Response(BaseModel):
    status_code: int
    detail: Optional[Any]
    message: str
    success: bool = False

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "detail": "Sample data",
                "message": "Ok",
                "success": True
            }
        }
