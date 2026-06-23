from pydantic import BaseModel, EmailStr
import uuid

# Token Schemas
class TokenPayload(BaseModel):
    sub: uuid.UUID
    sid: uuid.UUID
    type: str
    exp: int
    iat: int
    jti: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

# Auth schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


