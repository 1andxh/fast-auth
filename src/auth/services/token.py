from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.security import Security
from src.auth.services import RefreshTokenService, SessionService
from src.auth.repositories.session import SessionRepository
from src.auth.utils import create_access_token
from src.core.exceptions import (
    ExpiredTokenError,
    InvalidRefreshToken,
    RefreshTokenReuseError,
    SessionNotFoundError,
)
from src.core.logging.logger import logger


@dataclass(slots=True, frozen=True)
class AccessTokens:
    access_token: str
    refresh_token: str


class TokenService:
    def __init__(
        self,
        session: AsyncSession,
        session_service: SessionService,
        sessions_repo: SessionRepository,
        refresh_token_service: RefreshTokenService,
        security: Security,
    ) -> None:
        self.session_service = session_service
        self.refresh_token_service = refresh_token_service
        self.session = session
        self.sessions_repo = sessions_repo
        self.security = security

    async def issue_token_pair(
        self, user: User, user_agent: str | None = None, ip_address: str | None = None
    ) -> AccessTokens:
        session = await self.session_service.create_session(
            user_id=user.id, user_agent=user_agent, ip_address=ip_address
        )
        refresh_token = await self.refresh_token_service.create_refresh_token(
            session_id=session.id
        )
        access_token = create_access_token(user_id=user.id, session_id=session.id)

        return AccessTokens(
            access_token=access_token, refresh_token=refresh_token.raw_token
        )

    async def refresh_tokens(self, refresh_token: str) -> AccessTokens:
        stored_token = await self.refresh_token_service.get_token_by_hash(refresh_token)
        if not stored_token:
            raise InvalidRefreshToken()

        if stored_token.is_revoked:
            await self.refresh_token_service.revoke_token_family(stored_token.family_id)
            await self.session_service.revoke_session(stored_token.session_id)

            await self.session.commit()
            logger.warning(
                "refresh_token_reuse_detected",
                family_id=str(stored_token.family_id),
                session_id=str(stored_token.session_id),
            )
            raise RefreshTokenReuseError()

        elif stored_token.expires_at <= datetime.now(timezone.utc):
            raise ExpiredTokenError()

        session = await self.sessions_repo.find_by_id(stored_token.session_id)
        if not session:
            raise SessionNotFoundError()
        await self.session_service.validate_session(session)

        refreshed_token = await self.refresh_token_service.rotate_refresh_token(
            stored_token.id
        )
        access_token = create_access_token(
            user_id=session.user_id, session_id=session.id
        )

        logger.info("token_refreshed", session_id=str(session.id))

        return AccessTokens(
            access_token=access_token, refresh_token=refreshed_token.raw_token
        )

    async def logout(self, token: str) -> None:
        stored_hash = await self.refresh_token_service.get_token_by_hash(token=token)
        if not stored_hash:
            return

        session_id = stored_hash.session_id
        family_id = stored_hash.family_id

        await self.session_service.revoke_session(session_id=session_id)
        await self.refresh_token_service.revoke_token_family(family_id=family_id)

        logger.info("user_logged_out", session_id=str(session_id))
        await self.session.commit()
