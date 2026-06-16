from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.users import User
from src.users.services import UserService as user_service
from .schemas import TokenPayload
from .services import SessionService, TokenService
from .models import UserSession
from .utils import validate_access_token
from src.core.exceptions import InvalidTokenError, ExpiredTokenError

security =  HTTPBearer()
async def get_current_token(credentials: HTTPAuthorizationCredentials =  Depends(security)) -> TokenPayload:

    token = credentials.credentials
    payload = validate_access_token(token=token)

    if not payload:
        raise InvalidTokenError()
    
    return payload


async def get_current_session(service: SessionService, payload: TokenPayload = Depends(get_current_token)) -> UserSession:
    
    session = await service.get_session_by_id(payload.sid)
    # if session:
    await service.validate_session(session) if session else None
    
    




async def get_current_user(session: UserSession = Depends(get_current_session)) -> User:
    pass

