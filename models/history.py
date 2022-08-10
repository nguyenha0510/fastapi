import datetime
from beanie import Document
from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


class ActionEnum(str, Enum):
    edit = 'edit'
    delete = 'delete'
    reject = 'reject'
    mark = 'mark'
    approve = 'approve'


class History(Document):
    parent_id: str
    time_action: Optional[datetime.datetime] = None
    action_name: ActionEnum
    actor: str

    class Collection:
        name = "history"

    class Config:
        orm_mode = True,
        schema_extra = {
            "example": {
                "object_id": "7fgh8ew7f8sdh7cew7",
                "time_action": "2022/19/07 10:31:14",
                "action_name": "reject",
                "actor": "78yc8h348df23h89dh2",
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
