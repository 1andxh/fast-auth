from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
import uuid
from src.users.services import UserService
from .security import Security
from src.users import User
from src.core.exceptions import InvalidCredentialsError, InactiveUserError


@dataclass(frozen=True)
class AuthToken:
    access_token: str
    refresh_token: str



class AuthService:
    def __init__(self, user_service: UserService, security: Security) -> None:
        self.user_service = user_service
        self.security = security

    async def register(self, session: AsyncSession, email: str, password: str) -> User:
        password_hash = self.security.hash_password(password=password)
        user = await self.user_service.create_user(session=session, email=email, password_hash=password_hash)
        await session.commit()
        await session.refresh(user)

        return user
    
    async def authenticate(self, session: AsyncSession, email: str, password: str) -> User:
        user = await self.user_service.get_by_email(session, email)
        if user is None:
            raise InvalidCredentialsError()
        valid_password = self.security.verify_password(user.hashed_password, password)
        if not valid_password:
            raise InvalidCredentialsError()
        if not user.is_active:
            raise InactiveUserError() 
        return user
        


class SessionService:
    def __init__(self, session: AsyncSession, ) -> None:
        self.session = session

    async def create_session(self, user_id: uuid.UUID):
        pass
