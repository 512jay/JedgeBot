# /backend/auth/schemas.py
# Pydantic models for user input/output validation

from pydantic import BaseModel, EmailStr, ConfigDict, Field
from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Optional


# -------------------------------------------------------------------
# Enums
# -------------------------------------------------------------------
class UserRole(str, Enum):
    trader = "trader"
    client = "client"
    manager = "manager"
    enterprise = "enterprise"


class UserStatus(str, Enum):
    active = "active"
    grace = "grace"
    downgraded = "downgraded"
    banned = "banned"
    deactivated = "deactivated"


# -------------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=6, description="Password must be at least 6 characters"
    )
    role: UserRole
    username: Optional[str]


class LoginRequest(BaseModel):
    email: str
    password: str


class EmailRequest(BaseModel):
    email: EmailStr


# -------------------------------------------------------------------
# Response Schemas
# -------------------------------------------------------------------
class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    status: UserStatus
    created_at: datetime
    last_login: Optional[datetime]
    username: Optional[str]

    model_config = ConfigDict(from_attributes=True)
