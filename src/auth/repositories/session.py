import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models.session import UserSession


class SessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(self, session_id: uuid.UUID) -> UserSession | None:
        return await self.session.get(UserSession, session_id)

    async def create(self, user_session: UserSession) -> None:
        self.session.add(user_session)
        await self.session.flush()

    async def revoke(self, user_session: UserSession) -> None:
        user_session.revoked_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def revoke_all_for_user(self, user_id: uuid.UUID) -> None:
        pass
        # needed for password resets, logout of all devices, admin action, etc
