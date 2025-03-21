# /backend/data/database/auth/auth_services.py
# Business logic layer for authentication actions and workflows.

from datetime import datetime
from sqlalchemy.orm import Session
from backend.data.database.auth.models import User, UserRole
from backend.data.database.auth.auth_queries import get_user_by_email


def create_user(
    db: Session, email: str, password_hash: str, role: UserRole = UserRole.FREE
) -> User:
    """
    Creates a new user in the database if the email is not already taken.

    Args:
        db (Session): SQLAlchemy database session
        email (str): The user's email address
        password_hash (str): Hashed password (bcrypt)
        role (UserRole): The role to assign the user (default is FREE)

    Returns:
        User: The newly created user object

    Raises:
        ValueError: If a user with the given email already exists
    """
    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError("User with this email already exists.")

    user = User(email=email, password_hash=password_hash, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_last_login(db: Session, user: User) -> User:
    """
    Updates the last_login timestamp for the user.

    Args:
        db (Session): SQLAlchemy session
        user (User): User object to update

    Returns:
        User: The updated user object
    """
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user: User) -> User:
    """
    Deactivates a user account.

    Args:
        db (Session): SQLAlchemy session
        user (User): User to deactivate

    Returns:
        User: The updated user object
    """
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def change_user_role(db: Session, user: User, new_role: UserRole) -> User:
    """
    Changes the role of a user.

    Args:
        db (Session): SQLAlchemy session
        user (User): User to update
        new_role (UserRole): New role to assign

    Returns:
        User: The updated user object
    """
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(
    db: Session, email: str, password_hash: str, role: UserRole = UserRole.FREE
) -> User:
    """
    Retrieves a user by email or creates a new one if not found.

    Args:
        db (Session): SQLAlchemy session
        email (str): Email to search for
        password_hash (str): Hashed password (if new user)
        role (UserRole): Role to assign if created

    Returns:
        User: The existing or newly created user object
    """
    user = get_user_by_email(db, email)
    if user:
        return user
    return create_user(db, email, password_hash, role)
