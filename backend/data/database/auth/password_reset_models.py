# /backend/data/database/auth/password_reset_models.py
# Defines the PasswordResetToken table for managing password reset flows.

from sqlalchemy import String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime, timedelta
import uuid


class PasswordResetBase(DeclarativeBase):
    """Base for password reset models."""

    pass


class PasswordResetToken(PasswordResetBase):
    __tablename__ = "password_reset_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key for the reset token entry",
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        comment="User the reset token is associated with",
    )

    token: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True, comment="Secure random token"
    )

    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(minutes=30),
        comment="Token expiration timestamp",
    )

    used: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Whether this token has been used already"
    )
