# File: backend/models.py
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.auth_database import Base

import uuid


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(10), nullable=False, default="client")
    subscription_plan = Column(String(20), default="free")
    created_at = Column(TIMESTAMP, server_default="NOW()")
    updated_at = Column(TIMESTAMP, server_default="NOW()")


class ClientAccount(Base):
    __tablename__ = "client_accounts"

    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    broker_name = Column(String(50), nullable=False)
    account_number = Column(String(100), nullable=False)
