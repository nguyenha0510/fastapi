from beanie import Document
from pydantic import BaseModel
from typing import Optional, Any


class GroupUser(Document):
    description: Optional[Any] = None
    parent: Optional[Any] = None
    active: Optional[Any] = None
    created_time: Optional[Any] = None
    parent_name: Optional[Any] = None
    ancestors: Optional[Any] = None
    name: Optional[Any] = None
    tenant_id: Optional[Any] = None
    updated_time: Optional[Any] = None
    parent_id: Optional[Any] = None
    role: Optional[Any] = None
    expired_time: Optional[Any] = None
    alert_time: Optional[Any] = None
    alert_interval: Optional[Any] = None
    last_notify_expired_time: Optional[Any] = None
    industry: Optional[Any] = None

    class Collection:
        name = "group_user"

    class Config:
        orm_mode = True,


class GroupUserShortView(BaseModel):
    description: Optional[Any] = None
    parent: Optional[Any] = None
    active: Optional[Any] = None
    created_time: Optional[Any] = None
    parent_name: Optional[Any] = None
    ancestors: Optional[Any] = None
    name: Optional[Any] = None
    tenant_id: Optional[Any] = None
    updated_time: Optional[Any] = None
    parent_id: Optional[Any] = None
    role: Optional[Any] = None
    expired_time: Optional[Any] = None
    alert_time: Optional[Any] = None
    alert_interval: Optional[Any] = None
    last_notify_expired_time: Optional[Any] = None
    industry: Optional[Any] = None
