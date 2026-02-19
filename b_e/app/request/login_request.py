from typing import Annotated

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: Annotated[
        str,
        Field(..., min_length=1, description="Tên đăng nhập không được để trống")
    ]
    password: Annotated[
        str,
        Field(..., min_length=1, description="Mật khẩu không được để trống")
    ]