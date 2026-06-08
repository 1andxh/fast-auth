from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
import uuid
from src.users.services import UserService
from .security import Security
from src.users import User
from src.core.exceptions import InvalidCredentialsError, InactiveUserError, SessionRevokedError, SessionExpiredError
from .models import UserSession
from src.core.config import settings
from datetime import datetime, timezone, timedelta

# @dataclass(frozen=True)
# class AuthToken:
#     access_token: str
#     refresh_token: str

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
    SESSION_LIFETIME = settings.SESSION_LIFETIME_DAYS

    def __init__(self, session: AsyncSession, ) -> None:
        self.session = session

    async def create_session(self, user_id: uuid.UUID, user_agent: str | None = None, ip_address: str | None = None) -> UserSession:
        expires_at = datetime.now(timezone.utc) + timedelta(days=self.SESSION_LIFETIME)
        new_session = UserSession(
            user_id=user_id, user_agent=user_agent, ip_address=ip_address, expires_at=expires_at
        )
        self.session.add(new_session)

        await self.session.flush()
        return new_session

    async def get_session_by_id(self, session_id: uuid.UUID) -> UserSession | None:
        return await self.session.get(UserSession,session_id)
    
    async def revoke_session(self, user_session: UserSession) -> None:
        user_session.revoked_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def validate_session(self, user_session: UserSession) -> bool:
        now = datetime.now(timezone.utc)
        if user_session.revoked_at is not None:
            raise SessionRevokedError()
        if now >=  user_session.expires_at:
            raise SessionExpiredError()
        
        # slide session window if user is active ?
        return True
        

class RefreshTokenService:
    @dataclass(slots=True, frozen=True)
    class RefreshTokenResult:
        refresh_token: RefreshToken # type: ignore
        raw_token: str


    def __init__(self, security: Security) -> None:
        self.security = security

    async def create_refresh_token(self):...

    async def get_refresh_token(self):...

    async def rotate_refresh_token(self):...

    async def revoke_refresh_token(self):...

    async def revoke_token_family(self):...