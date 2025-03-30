# /backend/auth/tests/test_auth_services.py
# Unit tests for auth service functions using real database session.

import pytest
import uuid
from sqlalchemy.orm import Session
from backend.auth.auth_services import (
    hash_password,
    verify_password,
    create_user,
    get_or_create_user,
    deactivate_user,
    update_user_password,
    change_user_role,
)
from backend.auth.auth_models import UserRole, UserStatus
from backend.auth.auth_queries import get_user_by_email


@pytest.fixture
def test_email() -> str:
    """Generate a unique test email."""
    return f"testuser_{uuid.uuid4()}@example.com"


def test_hash_and_verify_password():
    password = "securepassword123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)


def test_create_user(get_db_session: Session, test_email: str):
    user = create_user(
        get_db_session, test_email, hash_password("pass"), role=UserRole.client
    )
    assert user.email == test_email
    assert user.role == UserRole.client
    assert user.status == UserStatus.active

    # Cleanup
    get_db_session.delete(user)
    get_db_session.commit()


def test_get_or_create_user(get_db_session: Session, test_email: str):
    password_hash = hash_password("pass123")
    user1 = get_or_create_user(get_db_session, test_email, password_hash)
    user2 = get_or_create_user(get_db_session, test_email, password_hash)
    assert user1.id == user2.id

    # Cleanup
    get_db_session.delete(user1)
    get_db_session.commit()


def test_deactivate_user(get_db_session: Session, test_email: str):
    user = create_user(get_db_session, test_email, hash_password("pass"))
    deactivated = deactivate_user(get_db_session, user)
    assert deactivated.status == UserStatus.deactivated

    # Cleanup
    get_db_session.delete(user)
    get_db_session.commit()


def test_update_user_password(get_db_session: Session, test_email: str):
    user = create_user(get_db_session, test_email, hash_password("oldpass"))
    updated = update_user_password(get_db_session, str(user.id), "newpass")
    assert verify_password("newpass", updated.password_hash)

    # Cleanup
    get_db_session.delete(user)
    get_db_session.commit()


def test_change_user_role(get_db_session: Session, test_email: str):
    user = create_user(get_db_session, test_email, hash_password("pass"))
    updated = change_user_role(get_db_session, user, UserRole.manager)
    assert updated.role == UserRole.manager

    # Cleanup
    get_db_session.delete(user)
    get_db_session.commit()
