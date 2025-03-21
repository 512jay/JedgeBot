# /backend/data/database/auth/models.py
# Models for the authentication database using SQLAlchemy.

from sqlalchemy import Column, String, Boolean, TIMESTAMP, text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid
import enum


class AuthBase(DeclarativeBase):
    pass


class UserRole(enum.Enum):
    FREE = "free"
    CLIENT = "client"
    MANAGER = "manager"
    ENTERPRISE = "enterprise"


class User(AuthBase):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False, default=UserRole.FREE
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    last_login = Column(TIMESTAMP, nullable=True)
