from __future__ import annotations
from typing import TYPE_CHECKING
from src.db import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
    DateTime,
    func,
    CheckConstraint,
    Index,
)
from datetime import datetime, timezone

if TYPE_CHECKING:
    from src.users import User


class UserSession(Base):
    __tablename__ = "usersessions"

    __table_args__ = (
        CheckConstraint(
            "revoked_at IS NULL or revoked_at >= created_at",
            name="check_session_revocation",
        ),
        Index("ix_session_user_id", "user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)

    # relationships
    user: Mapped["User"] = relationship("User", back_populates="sessions")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="session", cascade="all, delete-orphan"
    )

    @property
    def is_active(self) -> bool:
        return (
            self.revoked_at is None 
            and self.expires_at > datetime.now(timezone.utc)
        )
        
    


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
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usersessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
    )

    family_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    parent_token_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
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
        "UserSession",
        back_populates="refresh_tokens",
    )
