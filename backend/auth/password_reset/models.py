from sqlalchemy import Column, DateTime, Boolean, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from backend.data.database.base import Base
from uuid import uuid4
from datetime import datetime


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token = Column(String, nullable=False, unique=True, comment="Secure random token")
    expires_at = Column(
        DateTime(timezone=True), nullable=False, comment="UTC expiration timestamp"
    )
    used = Column(
        Boolean, default=False, nullable=False, comment="Flag to prevent reuse"
    )
