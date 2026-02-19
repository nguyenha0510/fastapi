from typing import Annotated

from fastapi import HTTPException, APIRouter, status, Body

from b_e.app.request.login_request import LoginRequest
from b_e.app.response.login_response import LoginResponse

router = APIRouter()

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Đăng nhập người dùng",
    responses={
        400: {"description": "Invalid request"},
        401: {"description": "Thông tin đăng nhập không đúng"}
    }
)
async def login(
        credentials: Annotated[LoginRequest, Body(...)],
):
    if not credentials.username.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Null value for username"
        )

    if not credentials.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Null value for password"
        )

    if credentials.username == "admin" and credentials.password == "123456":
        # Thành công → trả token (thực tế nên dùng JWT)
        return {
            "access_token": "fake-jwt-token-abcxyz123",
            "token_type": "bearer"
        }

    # Thất bại
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Tên đăng nhập hoặc mật khẩu không đúng",
        headers={"WWW-Authenticate": "Bearer"},
    )