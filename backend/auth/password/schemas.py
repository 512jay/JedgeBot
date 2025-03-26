# /backend/auth/password/schemas.py
# Pydantic schemas for password reset endpoints

from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(
        ..., description="User email", json_schema_extra={"example": "user@example.com"}
    )


class ResetPasswordRequest(BaseModel):
    token: str = Field(
        ...,
        min_length=16,
        description="Reset token",
        json_schema_extra={"example": "abcd1234securetoken"},
    )
    new_password: str = Field(
        ...,
        min_length=8,
        description="New password",
        json_schema_extra={"example": "MyNewPass123"},
    )
