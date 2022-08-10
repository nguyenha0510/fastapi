from beanie import Document
from pydantic import BaseModel
from typing import Optional, Any


class Tag(Document):
    name: str

    class Collection:
        name = "tags"

    class Config:
        orm_mode = True,
        schema_extra = {
            "example": {
                "name": "security"
            }
        }


class TagShortView(BaseModel):
    name: str


class Response(BaseModel):
    status_code: int
    detail: Optional[Any]
    message: str
    success: bool

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "detail": "Sample data",
                "message": "Ok",
                "success": True
            }
        }
