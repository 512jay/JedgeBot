# /backend/data/database/auth/password_reset_service.py
# Logic for creating and validating password reset tokens.

import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.data.database.auth.password_reset_models import PasswordResetToken
from backend.data.database.auth.models import User


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
        expires_at=datetime.utcnow() + timedelta(minutes=30),
        used=False,
    )

    db.add(reset_entry)
    db.commit()
    db.refresh(reset_entry)
    return token


def validate_password_reset_token(db: Session, token: str) -> User:
    """
    Validates a password reset token and returns the associated user.

    Args:
        db (Session): SQLAlchemy session
        token (str): The reset token

    Returns:
        User: The user linked to the valid token

    Raises:
        ValueError: If token is invalid, expired, or already used
    """
    reset_token = db.query(PasswordResetToken).filter_by(token=token).first()

    if not reset_token:
        raise ValueError("Invalid or unknown token")

    if reset_token.used:
        raise ValueError("Token has already been used")

    if reset_token.expires_at < datetime.utcnow():
        raise ValueError("Token has expired")

    return db.query(User).filter_by(id=reset_token.user_id).one()


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
