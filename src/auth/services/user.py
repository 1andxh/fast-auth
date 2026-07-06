import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DuplicateEmailError

from ..models.user_model import User
from src.auth.utils import normalize_email


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        normalized_email = normalize_email(email)
        stmt = await self.session.execute(
            select(User).where(User.email == normalized_email)
        )
        return stmt.scalar_one_or_none()

    async def get_by_id(self, id: uuid.UUID) -> User | None:
        return await self.session.get(User, id)

    async def create_user(self, email: str, password_hash: str) -> User:
        email = normalize_email(email)
        existing_user = await self.get_by_email(email)
        if existing_user:
            raise DuplicateEmailError()
        new_user = User(email=email, hashed_password=password_hash)
        self.session.add(new_user)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            raise DuplicateEmailError() from exc
        return new_user

    async def verify_user(self): ...

    async def deactivate_user(self): ...
