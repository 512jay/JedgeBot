# /conftest.py
# Shared test fixtures for FastAPI app, database session, and test user creation.

import uuid
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.main import app
from backend.auth.auth_services import create_user, hash_password
from backend.auth.auth_models import User, UserRole
from backend.data.database.db import get_db
from tests.utils.user_factory import random_email, random_password
from backend.notifications import email_service


@pytest.fixture(autouse=True)
def patch_send_email(monkeypatch):
    def dummy_send_email(to, subject, body):
        print(f"[MOCK EMAIL] To: {to} | Subject: {subject} | Body: {body[:60]}...")

    monkeypatch.setattr(email_service, "send_email", dummy_send_email)


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Provides a TestClient instance for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def unique_username():
    return f"tester_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="function")
def get_db_session() -> Generator[Session, None, None]:
    """Yields a real SQLAlchemy DB session for use in tests."""
    db_gen = get_db()
    db = next(db_gen)
    try:
        yield db
    finally:
        db.close()


def create_test_user(db: Session, role: UserRole) -> dict:
    """
    Helper function to create a user in the database for testing.

    Returns:
        dict: contains email, plaintext password, and user ID
    """
    email = random_email()
    password = random_password()
    password_hash = hash_password(password)
    user = create_user(db, email=email, password_hash=password_hash, role=role)
    return {"email": email, "password": password, "id": user.id}


@pytest.fixture(scope="function")
def free_user(get_db_session: Session) -> Generator[dict, None, None]:
    """Creates and cleans up a test user with 'free' role."""
    user = create_test_user(get_db_session, UserRole.free)
    yield user
    get_db_session.query(User).filter(User.id == user["id"]).delete()
    get_db_session.commit()


@pytest.fixture(scope="function")
def client_user(get_db_session: Session) -> Generator[dict, None, None]:
    """Creates and cleans up a test user with 'client' role."""
    user = create_test_user(get_db_session, UserRole.client)
    yield user
    get_db_session.query(User).filter(User.id == user["id"]).delete()
    get_db_session.commit()


@pytest.fixture(scope="function")
def manager_user(get_db_session: Session) -> Generator[dict, None, None]:
    """Creates and cleans up a test user with 'manager' role."""
    user = create_test_user(get_db_session, UserRole.manager)
    yield user
    get_db_session.query(User).filter(User.id == user["id"]).delete()
    get_db_session.commit()


@pytest.fixture
def captured_email(monkeypatch):
    sent_email = {}

    def mock_send_email(to, subject, body):
        sent_email["to"] = to
        sent_email["subject"] = subject
        sent_email["body"] = body
        print(f"[MOCK EMAIL] To: {to} | Subject: {subject} | Body: {body[:60]}...")

    monkeypatch.setattr(email_service, "send_email", mock_send_email)
    return sent_email
