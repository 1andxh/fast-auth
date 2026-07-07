from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.core.exceptions import DuplicateEmailError
from ..utils import normalize_email
from ..models import User

import uuid


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == normalize_email(email))
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self.session.get(User, user_id)

    async def create_user(self, user: User) -> None:
        self.session.add(user)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            raise DuplicateEmailError() from exc
