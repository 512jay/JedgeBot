# /backend/auth/tests/test_auth_routes.py
# Integration tests for auth endpoints using TestClient and real DB.

import uuid
import pytest
from fastapi.testclient import TestClient
from backend.auth.auth_models import UserRole
from backend.data.database.db import get_db
from backend.auth.auth_queries import get_user_by_email
from backend.user.user_models import UserProfile


@pytest.fixture
def unique_email():
    return f"testuser_{uuid.uuid4()}@example.com"


@pytest.fixture
def unique_username():
    return f"tester_{uuid.uuid4().hex[:8]}"


def test_register_and_login_flow(
    client: TestClient, get_db_session, unique_email: str, unique_username: str
):
    # Register
    payload = {
        "email": unique_email,
        "password": "secure123",
        "role": "client",
        "username": unique_username,
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200

    # Login
    login_payload = {"email": unique_email, "password": "secure123"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    client.cookies.update(response.cookies)

    response = client.get("/auth/check")
    assert response.status_code == 200
    assert response.json()["authenticated"] is True

    # Cleanup
    db = next(get_db())
    user = get_user_by_email(db, unique_email)
    if user:
        db.query(UserProfile).filter_by(user_id=user.id).delete()
        db.delete(user)
    db.commit()


def test_refresh_logout_me_flow(
    client: TestClient, get_db_session, unique_email: str, unique_username: str
):
    # Register and login to get cookies
    payload = {
        "email": unique_email,
        "password": "secure123",
        "role": "client",
        "username": unique_username,
    }
    client.post("/auth/register", json=payload)
    login_payload = {"email": unique_email, "password": "secure123"}
    response = client.post("/auth/login", json=login_payload)
    client.cookies.update(response.cookies)

    # /me
    response = client.get("/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == unique_email

    # /refresh
    response = client.post("/auth/refresh")
    assert response.status_code == 200
    assert "access_token" in response.cookies

    # /logout
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"

    # Cleanup
    db = next(get_db())
    user = get_user_by_email(db, unique_email)
    if user:
        db.query(UserProfile).filter_by(user_id=user.id).delete()
        db.delete(user)
    db.commit()
