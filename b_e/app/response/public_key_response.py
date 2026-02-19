from pydantic import BaseModel

class PublicKeyResponse(BaseModel):
    public_key: str
    format: str = "PEM"
    algorithm: str = "RS256"
    message: str = "This public key is safe to share publicly"