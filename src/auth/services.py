from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
import uuid
from src.users.services import UserService
from .security import Security
from src.users import User
from src.core.exceptions import InvalidCredentialsError, InactiveUserError, SessionRevokedError, SessionExpiredError, SessionNotFoundError, RefreshTokenNotFoundError, RefreshTokenAlreadyRevokedError, RefreshTokenReuseError, InvalidRefreshToken, ExpiredTokenError
from .models import UserSession, RefreshToken
from src.core.config import settings
from datetime import datetime, timezone, timedelta
from sqlalchemy import update, select, func
from src.auth.utils import create_access_token, validate_access_token, decode_token


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
    
    async def revoke_session(self, session_id: uuid.UUID) -> None:
        session = await self.get_session_by_id(session_id)
        if session:
            session.revoked_at = datetime.now(timezone.utc)
            await self.session.flush()


    async def validate_session(self, user_session: UserSession) -> bool:
        now = datetime.now(timezone.utc)
        if user_session.revoked_at is not None:
            raise SessionRevokedError()
        if now >=  user_session.expires_at:
            raise SessionExpiredError()
        
        # slide session window if user is active ?
        return True
        


@dataclass(slots=True, frozen=True)
class RefreshTokenResult:
    refresh_token: RefreshToken 
    raw_token: str

class RefreshTokenService:
    def __init__(self, security: Security, session: AsyncSession, session_service: SessionService) -> None:
        self.security = security
        self.session =  session
        self.session_service =  session_service

    async def create_refresh_token(self, session_id: uuid.UUID,family_id: uuid.UUID | None = None) -> RefreshTokenResult:
        user_session = await self.session_service.get_session_by_id(session_id)
        if not user_session:
            raise SessionNotFoundError()
        raw_token = self.security.generate_refresh_token()
        hashed_token = self.security.hash_refresh_token(raw_token)

        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        token = RefreshToken(session_id=user_session.id, token_hash=hashed_token, family_id=family_id or uuid.uuid4(), expires_at=expires_at)

        self.session.add(token)
        await self.session.flush()

        return RefreshTokenResult(refresh_token=token, raw_token=raw_token)
    
    async def get_refresh_token(self, token_id: uuid.UUID) -> RefreshToken | None :
        return await self.session.get(RefreshToken, token_id)
    
    async def get_token_by_hash(self, token: str) -> RefreshToken | None:
        token_hash = self.security.hash_refresh_token(token=token)
        stmt = await self.session.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        return stmt.scalar_one_or_none()
    
    async def rotate_refresh_token(self, token_id: uuid.UUID) -> RefreshTokenResult:
        old_token =  await self.get_refresh_token(token_id)
        if not old_token:
            raise RefreshTokenNotFoundError()
        
        if old_token.is_revoked:
            await self.revoke_token_family(old_token.family_id)
            raise RefreshTokenReuseError()
        
        await self.revoke_refresh_token(old_token.id)

        new_token = await self.create_refresh_token(session_id=old_token.session_id, family_id=old_token.family_id)

        new_token.refresh_token.parent_token_id = old_token.id

        await self.session.flush()
        return new_token

    async def revoke_refresh_token(self, token_id: uuid.UUID) -> None:
        token =  await self.get_refresh_token(token_id)
        if not token:
            raise RefreshTokenNotFoundError()
        if token.is_revoked is True:
            raise RefreshTokenAlreadyRevokedError()
        
        token.revoked_at = datetime.now(timezone.utc)
        token.is_revoked = True

        await self.session.flush()

    async def revoke_token_family(self, family_id: uuid.UUID):
        now = datetime.now(timezone.utc)
        stmt = update(RefreshToken).where(RefreshToken.family_id == family_id).values(is_revoked=True, revoked_at=now)

        await self.session.execute(stmt)
        await self.session.flush()


@dataclass(slots=True, frozen=True)
class AccessTokens:
    access_token: str
    refresh_token: str

class TokenService:
    def __init__(self, session: AsyncSession, session_service: SessionService, refresh_token_service: RefreshTokenService, security: Security) -> None:
        self.session_service = session_service
        self.refresh_token_service = refresh_token_service
        self.security = security
        self.session = session

    async def issue_token_pair(self, user: User, user_agent: str | None = None, ip_address: str | None = None) -> AccessTokens:
        session = await self.session_service.create_session(user_id=user.id, user_agent=user_agent, ip_address=ip_address)
        refresh_token =  await self.refresh_token_service.create_refresh_token(session_id=session.id)
        access_token =  create_access_token(user_id=user.id, session_id=session.id)

        return AccessTokens(access_token=access_token, refresh_token=refresh_token.raw_token)

    async def refresh_tokens(self, refresh_token: str) -> AccessTokens:
        token_hash = self.security.hash_refresh_token(refresh_token)
        stored_token = await self.refresh_token_service.get_token_by_hash(token_hash)
        if not stored_token:
            raise InvalidRefreshToken()

        if stored_token.is_revoked:
            await self.refresh_token_service.revoke_token_family(stored_token.family_id)
            await self.session_service.revoke_session(stored_token.session_id)

            await self.session.commit()
            raise RefreshTokenReuseError()

        elif stored_token.expires_at <= datetime.now(timezone.utc):
            raise ExpiredTokenError()
        
        session = await self.session_service.get_session_by_id(stored_token.session_id)
        if not session :
            raise SessionNotFoundError()
        await self.session_service.validate_session(session)

        refreshed_token = await self.refresh_token_service.rotate_refresh_token(stored_token.id)
        access_token = create_access_token(user_id=session.user_id, session_id=session.id)

        return AccessTokens(access_token=access_token, refresh_token=refreshed_token.raw_token)
    
    async def logout(self, token: str) -> None:
        token_hash = self.security.hash_refresh_token(token=token)
        stored_hash = await self.refresh_token_service.get_token_by_hash(token=token_hash)

        if not stored_hash:
            return
        
        session_id = stored_hash.session_id
        family_id = stored_hash.family_id

        await self.session_service.revoke_session(session_id=session_id)
        await self.refresh_token_service.revoke_token_family(family_id=family_id)

        await self.session.commit()







