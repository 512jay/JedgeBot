# /backend/waitlist/schemas.py

from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from uuid import UUID
from datetime import datetime

from backend.common.enums import UserRole


class WaitlistSubmission(BaseModel):
    name: str | None = None
    email: EmailStr
    role: UserRole = UserRole.trader
    feedback: str | None = None


class WaitlistResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    submitted_at: datetime
