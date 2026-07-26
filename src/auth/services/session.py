import uuid

from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.exceptions import (
    SessionExpiredError,
    SessionRevokedError,
)
from src.core.logging.logger import logger
from src.auth.models import UserSession
from src.auth.repositories.session import SessionRepository


class SessionService:
    SESSION_LIFETIME = settings.SESSION_LIFETIME_DAYS

    def __init__(self, sessions: SessionRepository) -> None:
        self.sessions = sessions

    async def create_session(
        self,
        user_id: uuid.UUID,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> UserSession:
        expires_at = datetime.now(timezone.utc) + timedelta(days=self.SESSION_LIFETIME)
        new_session = UserSession(
            user_id=user_id,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=expires_at,
        )

        await self.sessions.create(new_session)
        return new_session

    async def revoke_session(self, session_id: uuid.UUID) -> None:
        session = await self.sessions.find_by_id(session_id)
        if session:
            await self.sessions.revoke(session)

    async def validate_session(self, user_session: UserSession) -> bool:
        now = datetime.now(timezone.utc)
        if user_session.revoked_at is not None:
            raise SessionRevokedError()
        if now >= user_session.expires_at:
            raise SessionExpiredError()

        # slide session window if user is active ?
        return True
