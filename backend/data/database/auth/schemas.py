# /backend/data/database/auth/schemas.py
# Pydantic models for user input/output validation

from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from uuid import UUID
from datetime import datetime


class UserRole(str, Enum):
    FREE = "free"
    CLIENT = "client"
    MANAGER = "manager"
    ENTERPRISE = "enterprise"


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    last_login: datetime | None

    model_config = ConfigDict(from_attributes=True)  # Replaces orm_mode
