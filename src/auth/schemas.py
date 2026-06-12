from pydantic import BaseModel
import uuid


class TokenPayload(BaseModel):
    sub: uuid.UUID
    sid: uuid.UUID
    type: str
    exp: int
    iat: int
    jti: str
