# /backend/auth/auth_models.py
# Models for the authentication database using SQLAlchemy 2.0-style typing and PostgreSQL UUIDs.

from sqlalchemy import String, TIMESTAMP, text, Enum as PgEnum, DateTime, Column, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import uuid
from backend.data.database.base import Base
from backend.common.enums import UserRole, UserStatus


# -------------------------------------------------------------------
# Table: users
# -------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key (UUID)",
    )

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, comment="User's email address"
    )
    is_email_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)

    password_hash: Mapped[str] = mapped_column(
        String, nullable=False, comment="BCrypt-hashed password"
    )

    role: Mapped[UserRole] = mapped_column(
        PgEnum(
            UserRole, native_enum=False, values_callable=lambda x: [e.value for e in x]
        ),
        nullable=False,
        default=UserRole.trader,
        comment="Role of the user",
    )

    status: Mapped[UserStatus] = mapped_column(
        PgEnum(
            UserStatus,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=UserStatus.active,
        comment="Account status used for login gating",
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
        comment="Timestamp of user registration",
    )

    last_login: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True, comment="Last login timestamp"
    )

    profile = relationship("UserProfile", back_populates="user", uselist=False)
