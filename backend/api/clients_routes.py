# /backend/api/clients_routes.py
# Handles client-related routes, ensuring authentication.

from backend.data.database.auth.auth_schema import User  # ✅ Correct Import
from backend.api.auth_routes import (
    get_current_user,
)  # ✅ Import get_current_user for authentication
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.data.database.auth.auth_db import get_db  # ✅ Import get_db to access the database

router = APIRouter()


@router.get("/some-protected-route")
def some_protected_function(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """An example protected route"""
    return {"message": "Welcome!", "user": current_user.email}
