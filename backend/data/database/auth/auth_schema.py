# /backend/data/database/authorization/auth_schema.py
# Handles the User schema for the authentication database using SQLAlchemy.
# Defines authentication user model and provides methods for user retrieval.

from sqlalchemy import Column, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from backend.data.database.auth.auth_db_base import AuthBase
import uuid
from sqlalchemy.orm import Session


class User(AuthBase):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    last_login = Column(TIMESTAMP, nullable=True)

    @classmethod
    def get_user_by_email(cls, db_session: Session, email: str):
        return db_session.execute(
            select(cls).where(cls.email == email)
        ).scalar_one_or_none()
