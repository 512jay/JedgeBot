# /backend/waitlist/models.py
# SQLAlchemy models for the waitlist feature.

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from backend.data.database.db import Base
from backend.common.enums import UserRole


class WaitlistEntry(Base):
    __tablename__ = "waitlist_entries"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    role = Column(Enum(UserRole, name="userrole", create_type=False), nullable=False)
    feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
