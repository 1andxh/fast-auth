from typing import Annotated

from fastapi import Depends

from src.db.dependency import DbSession

from .refresh_token import RefreshTokenRepository
from .session import SessionRepository
from .user import UserRepository


async def get_user_respository(session: DbSession) -> UserRepository:
    return UserRepository(session)


UserRepoDep = Annotated[UserRepository, Depends(get_user_respository)]


async def get_session_repository(session: DbSession) -> SessionRepository:
    return SessionRepository(session)


SessionRepoDep = Annotated[SessionRepository, Depends(get_session_repository)]


async def get_refresh_token_repository(session: DbSession) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)


RefreshTokenRepoDep = Annotated[
    RefreshTokenRepository, Depends(get_refresh_token_repository)
]
