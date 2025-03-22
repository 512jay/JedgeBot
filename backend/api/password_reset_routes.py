# /backend/api/password_reset_routes.py
# FastAPI endpoints for initiating and completing password resets.

from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from backend.data.database.auth.auth_db import get_db
from backend.data.database.auth.auth_queries import get_user_by_email
from backend.data.database.auth.auth_services import hash_password
from backend.data.database.auth.password_reset_service import (
    create_password_reset_token,
    validate_password_reset_token,
    mark_token_as_used,
)
from backend.core.rate_limit import limiter

router = APIRouter()


# -----------------------------------------------------------------------------
# Schemas
# -----------------------------------------------------------------------------
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@router.post("/forgot-password")
@limiter.limit("3/minute")  # 👈 Optional: less frequent than login
def forgot_password(
    request: Request,  # 👈 add this
    request_data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Request a password reset link. Always returns 200 to prevent email enumeration.
    """
    user = get_user_by_email(db, request_data.email)
    if user:
        token = create_password_reset_token(db, user)
        # TODO: Send token via email (for now, print it)
        print(f"Password reset token for {user.email}: {token}")

    return {"message": "If that email exists, a reset link has been sent."}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Submit a valid reset token and a new password to complete the password reset.
    """
    try:
        user = validate_password_reset_token(db, request.token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    user.password_hash = hash_password(request.new_password)
    mark_token_as_used(db, request.token)
    db.commit()

    return {"message": "Password reset successfully."}


@router.get("/validate-token")
def validate_reset_token(token: str, db: Session = Depends(get_db)):
    try:
        # This reuses your existing logic
        _ = validate_password_reset_token(db, token)
        return {"message": "Token is valid."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
