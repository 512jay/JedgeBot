# /backend/auth/schemas.py
# Pydantic models for user input/output validation

from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserRole(str, Enum):
    free = "free"
    client = "client"
    manager = "manager"
    enterprise = "enterprise"


class UserStatus(str, Enum):
    active = "active"
    grace = "grace"
    downgraded = "downgraded"
    banned = "banned"
    deactivated = "deactivated"


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    status: UserStatus
    created_at: datetime
    last_login: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)  # Replaces orm_mode
