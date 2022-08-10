from pydantic import BaseModel
from typing import List, Optional, Any


class FilterStatistical(BaseModel):
    creator: Optional[str] = None
    tag: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "creator": "6a2sfe878sa8fsa8df8as",
                "tag": ["technology"],
            }
        }


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
