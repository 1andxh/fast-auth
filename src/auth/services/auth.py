from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
)

from src.core.logging.logger import logger
from src.auth.models import User
from src.auth.repositories.user import UserRepository
from src.auth.security import Security
from src.auth.utils import normalize_email


class AuthService:
    def __init__(
        self, session: AsyncSession, users: UserRepository, security: Security
    ) -> None:
        self.users = users
        self.session = session
        self.security = security

    async def register(self, email: str, password: str) -> User:
        password_hash = self.security.hash_password(password)
        user = User(email=normalize_email(email), hashed_password=password_hash)
        await self.users.create_user(user)
        await self.session.commit()
        await self.session.refresh(user)

        logger.info("user_registered", user_id=str(user.id), email=user.email)
        return user

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.users.find_by_email(email)
        if user is None:
            logger.warning("user_login_failed", email=email, reason="user_not_found")
            raise InvalidCredentialsError()
        valid_password = self.security.verify_password(user.hashed_password, password)
        if not valid_password:
            logger.info("user_login_failed", email=email, reason="invalid_password")
            raise InvalidCredentialsError()
        if not user.is_active:
            logger.warning(
                "user_login_failed", user_id=str(user.id), reason="inactive_user"
            )
            raise InactiveUserError()
        logger.info("user_login_success", user_id=str(user.id))
        return user
