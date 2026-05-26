from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class AuthToken:
    access_token: str
    refresh_token: str


class SessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_session(self, user_id: uuid.UUID):
        pass
