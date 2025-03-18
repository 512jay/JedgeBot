from passlib.context import CryptContext
import re
from fastapi import HTTPException

db_password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password securely using bcrypt."""
    return db_password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify hashed password."""
    return db_password_context.verify(plain_password, hashed_password)


def validate_password(password: str):
    """Ensure password meets security standards."""
    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long."
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter.",
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one lowercase letter.",
        )
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one number."
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one special character.",
        )
