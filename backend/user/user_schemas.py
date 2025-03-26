# /backend/user/user_schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserProfileCreate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    display_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None)
    timezone: Optional[str] = "UTC"


class UserProfileRead(UserProfileCreate):
    id: UUID
    user_id: UUID
    created_at: datetime
