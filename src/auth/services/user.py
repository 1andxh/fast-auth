import uuid

from src.core.exceptions import DuplicateEmailError

from ..models.user_model import User
from ..repositories.user import UserRepository


class UserService:
    def __init__(self, session: UserRepository) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        return await self.session.find_by_email(email)

    async def get_by_id(self, id: uuid.UUID) -> User | None:
        return await self.session.get_by_id(id)

    async def create_user(self, email: str, password_hash: str) -> User:
        existing_user = await self.get_by_email(email)
        if existing_user:
            raise DuplicateEmailError()
        new_user = User(email=email, hashed_password=password_hash)

        await self.session.create_user(new_user)
        return new_user

    async def verify_user(self): ...

    async def deactivate_user(self): ...
