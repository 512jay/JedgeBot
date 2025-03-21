# /backend/data/database/auth/models.py
# Models for the authentication database using SQLAlchemy 2.0-style typing and PostgreSQL UUIDs.

from sqlalchemy import String, Boolean, TIMESTAMP, text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid
import enum


# -----------------------------------------------------------------------------
# Base class for all authentication database models
# -----------------------------------------------------------------------------
class AuthBase(DeclarativeBase):
    """Declarative base for the auth database."""

    pass


# -----------------------------------------------------------------------------
# Enum: Defines valid user roles
# -----------------------------------------------------------------------------
class UserRole(enum.Enum):
    FREE = "free"  # Default unverified or limited user
    CLIENT = "client"  # Paid client with access to multiple brokerage accounts
    MANAGER = "manager"  # Can manage client accounts (with permission)
    ENTERPRISE = "enterprise"  # (Reserved) Future enterprise account tier


# -----------------------------------------------------------------------------
# Table: users
# -----------------------------------------------------------------------------
class User(AuthBase):
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

    password_hash: Mapped[str] = mapped_column(
        String, nullable=False, comment="BCrypt-hashed password"
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.FREE,
        comment="Role of the user",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, comment="Whether the account is active"
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("NOW()"),
        comment="Timestamp of user registration",
    )

    last_login: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True, comment="Last login timestamp"
    )
