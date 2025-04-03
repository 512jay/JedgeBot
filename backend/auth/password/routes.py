# /backend/auth/password/routes.py
# FastAPI routes for password reset: request, validate, and submit.

import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.auth.password.schemas import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from backend.auth.password.service import (
    create_password_reset_token,
    validate_token,
    mark_token_as_used,
)
from backend.auth.auth_services import get_user_by_email, update_user_password
from backend.data.database.db import get_db
from backend.core.settings import settings


router = APIRouter()


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if user:
        token = create_password_reset_token(db, user)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        # ✅ Actually send the email
        from backend.notifications import (
            smtp_service,
        )  # import here to avoid circular deps

        smtp_service.send_email(
            to=user.email,
            subject="Reset your password for Fordis Ludus",
            body=(
                f"You requested a password reset for your Fordis Ludus account.\n\n"
                f"Click the link below to set a new password:\n{reset_url}\n\n"
                f"If you didn’t request this, you can ignore this email."
            ),
        )

        if settings.TESTING:
            print("\n\n🔗 Password reset link for", request.email)
            print(reset_url)

    # Always return success message to avoid exposing user existence
    return {"message": "If that email is registered, a reset link was sent."}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Submit a valid reset token and a new password to complete the password reset.
    """
    try:
        user = validate_token(token=request.token, db=db)
        update_user_password(db, user.id, request.new_password)
        mark_token_as_used(db, request.token)
        return {"message": "Password reset successful."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/validate-token")
def validate_reset_token(token: str, db: Session = Depends(get_db)):
    try:
        _ = validate_token(token=token, db=db)
        return {"valid": True}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    except Exception as e:
        print("🔥 Unexpected error during token validation:", repr(e))
        traceback.print_exc()  # <-- full traceback
        raise HTTPException(status_code=500, detail="Server error during validation")
