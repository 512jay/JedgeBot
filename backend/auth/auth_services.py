# /backend/data/database/auth/auth_services.py
# Business logic layer for authentication actions and workflows.

from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from backend.auth.auth_models import User, UserRole
from backend.auth.auth_queries import get_user_by_email
from passlib.context import CryptContext
from backend.auth.auth_models import UserStatus
from backend.core.config import (
    SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Create a signed JWT refresh token."""
    expire = datetime.utcnow() + (
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return jwt.encode({"sub": user_id, "exp": expire}, SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_email_verification_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {"sub": email, "exp": expire, "type": "verify"}
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def create_user(
    db: Session, email: str, password_hash: str, role: UserRole = UserRole.trader
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
    user.status = UserStatus.deactivated
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    """
    Permanently deletes a user account from the database.

    Args:
        db (Session): SQLAlchemy session
        user (User): User to delete
    """
    db.delete(user)
    db.commit()


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
    db: Session, email: str, password_hash: str, role: UserRole = UserRole.trader
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


def update_user_password(db: Session, user_id: str, new_password: str) -> User:
    """
    Updates a user's password.

    Args:
        db (Session): SQLAlchemy session
        user_id (str): ID of the user to update
        new_password (str): New plaintext password

    Returns:
        User: The updated user object

    Raises:
        ValueError: If the user is not found
    """
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise ValueError("User not found")

    user.password_hash = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user
