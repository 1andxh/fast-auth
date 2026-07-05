import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


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


# Auth schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(RefreshRequest):
    pass


# user schema
class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    is_active: bool
    is_verified: bool
    created_at: datetime
