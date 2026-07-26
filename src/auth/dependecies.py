from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.annotations import SecurityDep
from src.core.exceptions import SessionNotFoundError, UserError
from src.db.dependency import DbSession

from .models import User, UserSession
from .repositories.dependencies import SessionRepoDep, UserRepoDep
from .schemas import TokenPayload
from .services import (
    AuthService,
    RefreshTokenService,
    SessionService,
    TokenService,
)
from .utils import validate_access_token

http_security = HTTPBearer()


async def get_session_service(sessions: SessionRepoDep) -> SessionService:
    return SessionService(sessions)


SessionServDep = Annotated[SessionService, Depends(get_session_service)]


async def get_auth_service(
    session: DbSession,
    user: UserRepoDep,
    security: SecurityDep,
) -> AuthService:
    return AuthService(session, user, security)


AuthServDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_refresh_service(
    session: DbSession, security: SecurityDep, service: SessionServDep
) -> RefreshTokenService:
    return RefreshTokenService(session, service, security)


RefreshServDep = Annotated[RefreshTokenService, Depends(get_refresh_service)]


async def get_token_service(
    session: DbSession,
    user_session: SessionServDep,
    refresh_service: RefreshServDep,
    security: SecurityDep,
) -> TokenService:
    return TokenService(session, user_session, refresh_service, security)


TokenServDep = Annotated[TokenService, Depends(get_token_service)]


async def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_security),
) -> TokenPayload:
    token = credentials.credentials
    payload = validate_access_token(token=token)
    return payload


async def get_current_session(
    service: SessionServDep,
    sessions: SessionRepoDep,
    payload: TokenPayload = Depends(get_current_token),
) -> UserSession:
    session = await sessions.find_by_id(payload.sid)
    if not session:
        raise SessionNotFoundError()

    await service.validate_session(session)
    return session


async def get_current_user(
    repo: UserRepoDep,
    user_session: UserSession = Depends(get_current_session),
) -> User:
    user = await repo.get_by_id(user_session.user_id)
    if not user or not user.is_active:
        raise UserError("User account is diasabled or missing")

    return user
