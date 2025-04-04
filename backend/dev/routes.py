# /backend/api/testing_routes.py
# ⚠️ TEST-ONLY ROUTES — Enabled only if settings.TESTING == True

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.settings import settings
from backend.data.database.db import get_db
from backend.auth.auth_models import User
from backend.auth.auth_services import get_user_by_email, delete_user
from backend.dev.cleanup import cleanup_password_reset_tokens

router = APIRouter()


@router.post("/auth/delete")
def delete_test_user(data: dict, db: Session = Depends(get_db)):
    """
    Deletes a test user by email — only available in test mode.
    """
    if not settings.TESTING:
        raise HTTPException(
            status_code=403, detail="This route is only enabled in test mode."
        )

    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required.")

    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    delete_user(db, user)
    return {"message": f"Test user '{email}' deleted successfully."}


@router.post("/cleanup/reset-tokens")
def dev_cleanup_tokens(db: Session = Depends(get_db)):
    deleted = cleanup_password_reset_tokens(db)
    return {"deleted": deleted}
