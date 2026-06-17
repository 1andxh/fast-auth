from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.users import User
from src.users.services import UserService 
from .schemas import TokenPayload
from .services import SessionService, TokenService
from .models import UserSession
from .utils import validate_access_token
from src.core.exceptions import InvalidTokenError, SessionNotFoundError, UserError

security =  HTTPBearer()

# service dependencies
async def get_session_service(session: AsyncSession = Depends(get_session)) -> SessionService:
    return SessionService(session)


async def get_current_token(credentials: HTTPAuthorizationCredentials =  Depends(security)) -> TokenPayload:

    token = credentials.credentials
    payload = validate_access_token(token=token)  
    return payload


async def get_current_session(service: SessionService = Depends(get_session_service), payload: TokenPayload = Depends(get_current_token)) -> UserSession:
    
    session = await service.get_session_by_id(payload.sid)
    if not session:
        raise SessionNotFoundError()
    
    await service.validate_session(session)
    return session


async def get_current_user(session: AsyncSession = Depends(get_session), user_session: UserSession = Depends(get_current_session), service: UserService = Depends(UserService)) -> User:
    user = await service.get_by_id(session=session, id=user_session.user_id)
    if not user or not user.is_active:
        raise UserError("User account is diasabled or missing")

    return user