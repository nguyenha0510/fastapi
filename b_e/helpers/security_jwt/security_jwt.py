from fastapi import Request, HTTPException, status
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import json
import base64
from datetime import datetime, timedelta, timezone
from pydantic import json

from b_e.config import config

async def generate_rsa_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Giá trị chuẩn và an toàn
        key_size=2048,  # 2048 hoặc 3072/4096
        backend=default_backend()  # Không cần chỉ định ở phiên bản mới, nhưng giữ cho tương thích
    )

    public_key = private_key.public_key()

    config['PRIVATE_KEY'] = private_key
    config['PUBLIC_KEY'] = public_key

def encode_cookie(data: dict):
    json_str = json.dumps(data, separators=(",", ":"))  # gọn nhất có thể
    plaintext = json_str.encode("utf-8")

    ciphertext = config['PUBLIC_KEY'].encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.urlsafe_b64encode(ciphertext).decode("utf-8")

def decode_cookie(request: Request):
    cookie = request.headers.get('cookie')
    if not cookie:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    else:
        list_value_creator = cookie.split("; ")
        if not any(value.startswith('access_token_cookie') for value in cookie.split("; ")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            for value in list_value_creator:
                if value.startswith('access_token_cookie'):
                    access_token = value.split('access_token_cookie=')
                    try:
                        ciphertext = base64.urlsafe_b64decode(access_token[1])
                        plaintext = config['PRIVATE_KEY'].decrypt(
                            ciphertext,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        )
                        data = json.loads(plaintext.decode("utf-8"))
                        if data.get('exp') < datetime.now(timezone.utc):
                            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                            )
                        else:
                            request.state.current_user = data.get('account')
                    except Exception:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                        )

def create_auth_cookie(account: str, days_valid: int = 1) -> str:
    """Tạo giá trị cookie đã mã hóa"""
    expire_at = int((datetime.now(timezone.utc) + timedelta(days=days_valid)).timestamp())
    data = {"account": account, "exp": expire_at}
    return encode_cookie(data)