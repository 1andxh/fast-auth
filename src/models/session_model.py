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
from sqlalchemy.dialects.postgresql import (
    UUID as PG_UUID,
    INET,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from src.db import Base


class Session(Base):
    __tablename__ = "sessions"

    __table_args__ = (
        CheckConstraint(
            "revoked_at IS NULL OR revoked_at >= created_at",
            name="chk_session_revocation_chronology",
        ),
        Index(
            "ix_sessions_user_id_is_revoked",
            "user_id",
            "is_revoked",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        INET,
        nullable=True,
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="sessions",
    )

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="session",
        cascade="all, delete-orphan",
    )
