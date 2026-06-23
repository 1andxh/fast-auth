from fastapi import Depends, HTTPException
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.db.dependency import DbSession
from src.users import User
from .schemas import TokenPayload
from .services import SessionService, AuthService, TokenService, RefreshTokenService
from .models import UserSession
from .utils import validate_access_token
from src.core.exceptions import InvalidTokenError, SessionNotFoundError, UserError
from src.auth.annotations import SecurityDep, UserServDep


http_security =  HTTPBearer()

async def get_session_service(session: DbSession) -> SessionService:
    return SessionService(session)

SessionServDep = Annotated[SessionService, Depends(get_session_service)]

# --- deps that build on the base ones ---
async def get_auth_service(session: DbSession, security: SecurityDep, user_service: UserServDep) -> AuthService:
    return AuthService(session, user_service, security)

AuthServDep = Annotated[AuthService, Depends(get_auth_service)]

async def get_refresh_service(session: DbSession, security: SecurityDep, service: SessionServDep) -> RefreshTokenService:
    return RefreshTokenService(session, service, security)

RefreshServDep = Annotated[RefreshTokenService, Depends(get_refresh_service)]

async def get_token_service(session: DbSession, user_session: SessionServDep, refresh_service: RefreshServDep, security: SecurityDep) -> TokenService:
    return TokenService(session, user_session, refresh_service, security)

TokenServDep = Annotated[TokenService, Depends(get_token_service)]


async def get_current_token(credentials: HTTPAuthorizationCredentials =  Depends(http_security)) -> TokenPayload:

    token = credentials.credentials
    payload = validate_access_token(token=token)  
    return payload


async def get_current_session(service: SessionServDep, payload: TokenPayload = Depends(get_current_token)) -> UserSession:
    
    session = await service.get_session_by_id(payload.sid)
    if not session:
        raise SessionNotFoundError()
    
    await service.validate_session(session)
    return session


async def get_current_user(service: UserServDep, user_session: UserSession = Depends(get_current_session), ) -> User:
    user = await service.get_by_id(id=user_session.user_id)
    if not user or not user.is_active:
        raise UserError("User account is diasabled or missing")

    return user