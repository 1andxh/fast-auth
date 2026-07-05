from src.db.dependency import DbSession
from .user import UserRepository
from .session import SessionRepository
from .refresh_token import RefreshTokenRepository


async def get_user_respository(session: DbSession) -> UserRepository:
    return UserRepository(session)


async def get_session_repository(session: DbSession) -> SessionRepository:
    return SessionRepository(session)


async def get_refresh_token_repository(session: DbSession) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)
