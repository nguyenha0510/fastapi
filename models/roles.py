from beanie import Document
from pydantic import BaseModel
from typing import Optional, Any


class Roles(Document):
    month: Optional[Any] = None
    permissions: Optional[Any] = None
    description: Optional[Any] = None
    role_id: Optional[Any] = None

    class Collection:
        name = "roles"

    class Config:
        orm_mode = True,

class RolesShortVIew(BaseModel):
    role_id: Optional[Any] = None