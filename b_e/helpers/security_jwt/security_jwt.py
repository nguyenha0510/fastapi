from datetime import timedelta, datetime, timezone
from typing import Optional

import jwt
from fastapi import Request, HTTPException, status
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from jwt import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError

from b_e.config import config

async def generate_rsa_key_pair(key_size=2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    # Public key (SubjectPublicKeyInfo PEM)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    config['PRIVATE_KEY'] = private_pem
    config['PUBLIC_KEY'] = public_pem

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
    ) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=config['ACCESS_TOKEN_EXPIRE_DAYS'])
    )

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    })

    encoded_jwt = jwt.encode(
        to_encode,
        config['PRIVATE_KEY'],
        algorithm=config['ALGORITHM']
    )
    return encoded_jwt

def create_auth_cookie(account: str, days_valid: int = config['ACCESS_TOKEN_EXPIRE_DAYS']) -> str:
    payload = {"account": account}
    return create_access_token(payload, timedelta(days=days_valid))


async def decode_and_verify_cookie(request: Request):
    cookie_header = request.headers.get("cookie")
    if not cookie_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    access_token = None
    for part in cookie_header.split("; "):
        if part.startswith("access_token_cookie="):
            access_token = part.split("=", 1)[1]
            break

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        payload = jwt.decode(
            access_token,
            config['PUBLIC_KEY'],
            algorithms=[config['ALGORITHM']],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "require": ["exp", "iat"],
            }
        )

        account = payload.get("account")
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        request.state.current_user = account
        return account

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except (InvalidSignatureError, InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

def encrypt_with_public_key(kwargs) -> str:
    if len(kwargs) > 190:
        raise ValueError(f"Dữ liệu quá lớn ({len(kwargs)} bytes). RSA 2048 chỉ mã hóa được ~190 byte.")

    ciphertext = config['PUBLIC_KEY'].encrypt(
        kwargs,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt_with_private_key(ciphertext: str):
    plaintext = config['PRIVATE_KEY'].decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return plaintext