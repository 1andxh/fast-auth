import uuid
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, token: RefreshToken) -> None:
        self.session.add(token)
        await self.session.flush()

    async def find_by_id(self, token_id: uuid.UUID) -> RefreshToken | None:
        return await self.session.get(RefreshToken, token_id)

    async def find_by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return stmt.scalar_one_or_none()

    async def revoke(self, token: RefreshToken) -> None:
        token.revoked_at = datetime.now(timezone.utc)
        token.is_revoked = True

        await self.session.flush()

    async def revoke_family(self, family_id: uuid.UUID) -> None:
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.family_id == family_id)
            .values(is_revoked=True, revoked_at=datetime.now(timezone.utc))
        )

        await self.session.execute(stmt)
        await self.session.flush()

    async def flush(self) -> None:
        return await self.session.flush()
