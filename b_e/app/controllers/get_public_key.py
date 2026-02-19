from fastapi import HTTPException, APIRouter
from b_e.app.response.public_key_response import PublicKeyResponse
from b_e.config import config

router = APIRouter()

@router.get("/public-key", response_model=PublicKeyResponse)
async def get_public_key():
    if not config['PUBLIC_KEY']:
        raise HTTPException(status_code=404, detail="Not have public key")

    return PublicKeyResponse(
        public_key= config['PUBLIC_KEY'].strip(),
        algorithm="RS256",
        message="Safe to expose. Used for encrypting data."
    )