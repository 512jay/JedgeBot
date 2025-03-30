# /backend/data/database/auth/auth_queries.py
# Queries for user management in the authentication database.

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.auth.auth_models import User, UserRole


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve a user by their email address.

    Args:
        db (Session): SQLAlchemy database session
        email (str): User's email address

    Returns:
        User or None: The user object if found, else None
    """
    return db.query(User).filter(func.lower(User.email) == email.lower()).first()


def get_user_by_id(db: Session, user_id: str) -> User | None:
    """
    Retrieve a user by their ID.

    Args:
        db (Session): SQLAlchemy database session
        user_id (str): User's UUID

    Returns:
        User or None: The user object if found, else None
    """
    return db.query(User).filter(User.id == user_id).first()


def list_users_by_role(db: Session, role: UserRole) -> list[User]:
    """
    List all users with a specific role.

    Args:
        db (Session): SQLAlchemy database session
        role (UserRole): Role to filter by

    Returns:
        List[User]: Users matching the given role
    """
    return db.query(User).filter(User.role == role).all()


def update_last_login(db: Session, user: User) -> User:
    """
    Update the last login time for a given user.

    Args:
        db (Session): SQLAlchemy database session
        user (User): The user object to update

    Returns:
        User: The updated user object
    """
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user
