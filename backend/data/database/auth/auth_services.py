# /backend/data/database/auth/auth_services.py
# Business logic layer for authentication actions and workflows.

from sqlalchemy.orm import Session
from backend.data.database.auth.models import User, UserRole
from backend.data.database.auth.auth_queries import get_user_by_email
from datetime import datetime
from typing import Optional


def create_user(
    db: Session, email: str, password_hash: str, role: UserRole = UserRole.FREE
) -> User:
    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError("User with this email already exists.")

    user = User(email=email, password_hash=password_hash, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_last_login(db: Session, user: User) -> User:
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user: User) -> User:
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def change_user_role(db: Session, user: User, new_role: UserRole) -> User:
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(
    db: Session, email: str, password_hash: str, role: UserRole = UserRole.FREE
) -> User:
    user = get_user_by_email(db, email)
    if user:
        return user
    return create_user(db, email, password_hash, role)
