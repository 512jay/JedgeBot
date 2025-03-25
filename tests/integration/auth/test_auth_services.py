# /tests/integration/auth/test_auth_services.py

import pytest
from sqlalchemy.orm import Session
from backend.auth.auth_services import (
    hash_password,
    verify_password,
    create_user,
    deactivate_user,
    change_user_role,
    get_or_create_user,
)
from backend.auth.models import User, UserRole
from backend.auth.auth_db import get_db
import uuid


def generate_unique_email() -> str:
    return f"unit_{uuid.uuid4().hex[:8]}@example.com"


def test_hash_and_verify_password() -> None:
    plain = "mytestpassword123"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed)


def test_create_user_and_get_or_create_user() -> None:
    email = generate_unique_email()
    password = "unitpass123"
    password_hash = hash_password(password)
    db_gen = get_db()
    db: Session = next(db_gen)

    # create user
    user = create_user(
        db, email=email, password_hash=password_hash, role=UserRole.CLIENT
    )
    assert user.email == email
    assert user.role == UserRole.CLIENT

    # get_or_create should return the same user
    same_user = get_or_create_user(db, email=email, password_hash=password_hash)
    assert same_user.id == user.id

    # cleanup
    db.delete(user)
    db.commit()
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_deactivate_user_and_change_role() -> None:
    email = generate_unique_email()
    password = "deactivateTest456"
    password_hash = hash_password(password)
    db_gen = get_db()
    db: Session = next(db_gen)

    user = create_user(db, email=email, password_hash=password_hash, role=UserRole.FREE)

    # change role
    updated_user = change_user_role(db, user, UserRole.MANAGER)
    assert updated_user.role == UserRole.MANAGER

    # deactivate user
    deactivated_user = deactivate_user(db, user)
    assert deactivated_user.is_active is False

    # cleanup
    db.delete(user)
    db.commit()
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_update_last_login_sets_timestamp() -> None:
    email = generate_unique_email()
    password = "logintestpass"
    password_hash = hash_password(password)
    db_gen = get_db()
    db: Session = next(db_gen)

    user = create_user(db, email=email, password_hash=password_hash)
    assert user.last_login is None

    # update last login
    from backend.auth.auth_services import update_last_login

    updated_user = update_last_login(db, user)
    assert updated_user.last_login is not None

    # cleanup
    db.delete(user)
    db.commit()
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_verify_password_fails_on_mismatch() -> None:
    correct_password = "correct_password"
    wrong_password = "wrong_password"
    hashed = hash_password(correct_password)
    assert not verify_password(wrong_password, hashed)



