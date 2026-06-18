from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.db.session import get_session
from src.db.dependency import session
from sqlalchemy.ext.asyncio import AsyncSession
from src.users import User
from src.users.services import UserService 
from .schemas import TokenPayload
from .services import SessionService, AuthService, TokenService, RefreshTokenService
from .models import UserSession
from .utils import validate_access_token
from .security import Security
from src.core.exceptions import InvalidTokenError, SessionNotFoundError, UserError
from typing import Annotated

security =  HTTPBearer()
# SessionServDep = 
# DbSession = 
# RefreshServDep = 
# UserServDep

# service dependencies
async def get_session_service(session: session) -> SessionService:
    return SessionService(session)

async def get_auth_service(session: session, auth_security: Security, user_service: UserService = Depends(UserService),) -> AuthService:
    return AuthService(session, user_service)

async def get_refresh_service(session: session, user_session):
    pass

async def get_token_service(session: session, user_session: SessionService, refresh_service: RefreshTokenService, auth_security: Security) -> TokenService:
    return TokenService(session, user_session, refresh_service,)


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