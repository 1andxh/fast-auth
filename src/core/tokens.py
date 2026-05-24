from datetime import datetime, timedelta, timezone
import uuid
import jwt

from src.core.config import settings
from src.schemas import TokenPayload
from src.core.exceptions import ExpiredTokenError, InvalidTokenError

JWT_SECRET = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRY_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(subject: uuid.UUID) -> str:
    now = datetime.now(timezone.utc)

    expiry = now + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)

    payload = {
        "sub": str(subject),
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expiry.timestamp()),
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError as exc:
        raise ExpiredTokenError("Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise InvalidTokenError("Invalid token") from exc


def validate_access_token(token: str) -> TokenPayload:
    payload = decode_token(token)
    if payload != "access":
        raise InvalidTokenError("Token is not an access token")
    return payload
