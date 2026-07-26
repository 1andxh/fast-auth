import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import RefreshToken
from src.auth.security import Security
from src.auth.services import SessionService
from src.core.config import settings
from src.core.exceptions import (
    RefreshTokenAlreadyRevokedError,
    RefreshTokenNotFoundError,
    RefreshTokenReuseError,
    SessionNotFoundError,
)


@dataclass(slots=True, frozen=True)
class RefreshTokenResult:
    refresh_token: RefreshToken
    raw_token: str


class RefreshTokenService:
    def __init__(
        self, session: AsyncSession, session_service: SessionService, security: Security
    ) -> None:
        self.session = session
        self.session_service = session_service
        self.security = security

    async def create_refresh_token(
        self, session_id: uuid.UUID, family_id: uuid.UUID | None = None
    ) -> RefreshTokenResult:
        user_session = await self.session_service.get_session_by_id(session_id)
        if not user_session:
            raise SessionNotFoundError()
        raw_token = self.security.generate_refresh_token()
        hashed_token = self.security.hash_refresh_token(raw_token)

        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        token = RefreshToken(
            session_id=user_session.id,
            token_hash=hashed_token,
            family_id=family_id or uuid.uuid4(),
            expires_at=expires_at,
        )

        self.session.add(token)
        await self.session.flush()

        return RefreshTokenResult(refresh_token=token, raw_token=raw_token)

    async def get_refresh_token(self, token_id: uuid.UUID) -> RefreshToken | None:
        return await self.session.get(RefreshToken, token_id)

    async def get_token_by_hash(self, token: str) -> RefreshToken | None:
        token_hash = self.security.hash_refresh_token(token=token)
        stmt = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return stmt.scalar_one_or_none()

    async def rotate_refresh_token(self, token_id: uuid.UUID) -> RefreshTokenResult:
        old_token = await self.get_refresh_token(token_id)
        if not old_token:
            raise RefreshTokenNotFoundError()

        if old_token.is_revoked:
            await self.revoke_token_family(old_token.family_id)
            raise RefreshTokenReuseError()

        await self.revoke_refresh_token(old_token.id)

        new_token = await self.create_refresh_token(
            session_id=old_token.session_id, family_id=old_token.family_id
        )

        new_token.refresh_token.parent_token_id = old_token.id

        await self.session.flush()
        return new_token

    async def revoke_refresh_token(self, token_id: uuid.UUID) -> None:
        token = await self.get_refresh_token(token_id)
        if not token:
            raise RefreshTokenNotFoundError()
        if token.is_revoked is True:
            raise RefreshTokenAlreadyRevokedError()

        token.revoked_at = datetime.now(timezone.utc)
        token.is_revoked = True

        await self.session.flush()

    async def revoke_token_family(self, family_id: uuid.UUID):
        now = datetime.now(timezone.utc)
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.family_id == family_id)
            .values(is_revoked=True, revoked_at=now)
        )

        await self.session.execute(stmt)
        await self.session.flush()
