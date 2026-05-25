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
from datetime import datetime

if TYPE_CHECKING:
    from src.models import User
    from src.models import RefreshToken


class Session(Base):
    __tablename__ = "sessions"

    __table_args__ = (
        CheckConstraint(
            "revoked_at IS NULL or revoked_at >= created_at",
            name="check_session_revocation",
        ),
        Index("ix_session_user_id_is_revoked", "user_id", "is_revoked"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    revoked_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # relationships
    user = relationship("User", back_populates="sessions")
    refresh_tokens = relationship(
        "RefreshToken", back_populates="session", cascade="all, delete-orphan"
    )
