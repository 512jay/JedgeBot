# /backend/data/database/auth/password_reset_models.py
# Defines the PasswordResetToken table for managing password reset flows.

from backend.auth.models import User, AuthBase  # ✅ Use AuthBase
from sqlalchemy import String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timedelta
import uuid


class PasswordResetToken(AuthBase):  # ✅ Unified declarative base
    __tablename__ = "password_reset_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key for the reset token entry",
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE",),
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

def test_reset_password_with_invalid_token_returns_400() -> None:
    db_gen = get_db()
    db: Session = next(db_gen)

    invalid_token = "this-token-does-not-exist"
    new_password = "DoesNotMatter123"

    # Attempt to reset with invalid token
    response = client.post(
        "/auth/reset-password",
        json={"token": invalid_token, "new_password": new_password}
    )

    assert response.status_code == 400
    assert "Invalid or unknown token" in response.json()["detail"]

    try:
        next(db_gen)
    except StopIteration:
        pass
