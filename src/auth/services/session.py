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


class SessionService:
    SESSION_LIFETIME = settings.SESSION_LIFETIME_DAYS

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

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
        self.session.add(new_session)

        await self.session.flush()
        return new_session

    async def get_session_by_id(self, session_id: uuid.UUID) -> UserSession | None:
        return await self.session.get(UserSession, session_id)

    async def revoke_session(self, session_id: uuid.UUID) -> None:
        session = await self.get_session_by_id(session_id)
        if session:
            session.revoked_at = datetime.now(timezone.utc)
            await self.session.flush()

    async def validate_session(self, user_session: UserSession) -> bool:
        now = datetime.now(timezone.utc)
        if user_session.revoked_at is not None:
            raise SessionRevokedError()
        if now >= user_session.expires_at:
            raise SessionExpiredError()

        # slide session window if user is active ?
        return True
