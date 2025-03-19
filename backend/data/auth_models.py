from sqlalchemy import Column, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from backend.data.auth_base import AuthBase
import uuid


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
