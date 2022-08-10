from pydantic import BaseModel
from typing import List, Optional, Any


class EmailData(BaseModel):
    subject: str
    addrs: List[str]
    body: str
    no_signature: bool = True

    class Config:
        schema_extra = {
            "example": {
                "subject": "test send mail",
                "addrs": ['is_hanv@viettelcyber.com', 'is_huyenst@viettelcyber.com'],
                "body": "Xin chao, toi la Ha. Day la Email test!",
                "no_signature": True,
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
