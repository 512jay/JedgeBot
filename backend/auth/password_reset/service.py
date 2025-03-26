# /backend/auth/password_reset/service.py
# Logic for creating and validating password reset tokens.


import secrets
from datetime import datetime, timedelta
from typing import Callable, Optional
from sqlalchemy.orm import Session
from backend.auth.password_reset.models import PasswordResetToken
from backend.auth.auth_models import User
from datetime import timezone


def create_password_reset_token(db: Session, user: User) -> str:
    """
    Generates a secure password reset token for a user and stores it in the database.

    Args:
        db (Session): SQLAlchemy session
        user (User): The user requesting a reset

    Returns:
        str: The generated token (to be sent to the user)
    """
    token = secrets.token_urlsafe(48)

    reset_entry = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        used=False,
    )

    db.add(reset_entry)
    db.commit()
    db.refresh(reset_entry)
    return token


def validate_token(
    token: str,
    db: Optional[Session] = None,
    lookup_token: Optional[Callable[[str], PasswordResetToken]] = None,
) -> User:
    """
    Validates a password reset token and returns the associated user.
    Accepts either a database session or a lookup function for testing.

    Args:
        token (str): The reset token
        db (Session, optional): SQLAlchemy session
        lookup_token (Callable, optional): Mockable token fetcher

    Returns:
        User: The user linked to the valid token

    Raises:
        ValueError: If token is invalid, expired, or already used
    """
    if lookup_token is not None:
        reset_token = lookup_token(token)
    elif db is not None:
        reset_token = db.query(PasswordResetToken).filter_by(token=token).first()
    else:
        raise ValueError("Either db or lookup_token must be provided")

    if not reset_token:
        raise ValueError("Invalid or unknown token")

    if reset_token.used:
        raise ValueError("Token has already been used")

    if reset_token.expires_at < datetime.now(timezone.utc):
        raise ValueError("Token has expired")

    if db is not None:
        user = db.query(User).filter_by(id=reset_token.user_id).first()
        if not user:
            raise ValueError("Associated user does not exist")
        return user


def mark_token_as_used(db: Session, token: str):
    """
    Marks a token as used so it cannot be reused.

    Args:
        db (Session): SQLAlchemy session
        token (str): The reset token to mark used
    """
    reset_token = db.query(PasswordResetToken).filter_by(token=token).first()
    if reset_token:
        reset_token.used = True
        db.commit()
