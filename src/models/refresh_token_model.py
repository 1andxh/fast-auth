from __future__ import annotations
from typing import TYPE_CHECKING
import uuid
from datetime import datetime
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from src.db import Base

if TYPE_CHECKING:
    from src.models import Session


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    __table_args__ = (
        CheckConstraint(
            "expires_at > created_at",
            name="chk_token_expiry",
        ),
        CheckConstraint(
            "revoked_at IS NULL OR revoked_at >= created_at",
            name="chk_token_revocation",
        ),
        Index(
            "ix_refresh_family_revoked",
            "family_id",
            "is_revoked",
        ),
        Index(
            "ix_refresh_expires_at",
            "expires_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
    )

    family_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
    )

    parent_token_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("refresh_tokens.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    session = relationship(
        "Session",
        back_populates="refresh_tokens",
    )
