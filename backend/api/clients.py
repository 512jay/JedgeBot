from backend.data.auth_models import User  # ✅ Correct Import
from backend.api.auth import (
    get_current_user,
)  # ✅ Import get_current_user for authentication
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.data.auth_database import get_db  # ✅ Import get_db to access the database

router = APIRouter()


@router.get("/some-protected-route")
def some_protected_function(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """An example protected route"""
    return {"message": "Welcome!", "user": current_user.email}
