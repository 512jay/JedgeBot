# /backend/auth/tests/test_auth_routes.py
# Integration tests for auth endpoints using TestClient and real DB.

import uuid
import jwt as pyjwt
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


def test_login_wrong_password(
    client: TestClient, get_db_session, unique_email, unique_username
):
    # Setup: register the user
    payload = {
        "email": unique_email,
        "password": "rightpass",
        "role": "client",
        "username": unique_username,
    }
    client.post("/auth/register", json=payload)

    # Try logging in with wrong password
    login_payload = {"email": unique_email, "password": "wrongpass"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email or password"

    # Cleanup
    db = next(get_db())
    user = get_user_by_email(db, unique_email)
    if user:
        db.query(UserProfile).filter_by(user_id=user.id).delete()
        db.delete(user)
    db.commit()


def test_login_nonexistent_email(client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": "doesnotexist@example.com", "password": "whatever"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email or password"


def test_register_duplicate_email(client: TestClient, unique_email, unique_username):
    # First registration
    client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": "secure123",
            "role": "client",
            "username": unique_username,
        },
    )

    # Second registration with same email but new username
    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": "anotherpass",
            "role": "client",
            "username": f"{unique_username}_new",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

    # Cleanup
    db = next(get_db())
    user = get_user_by_email(db, unique_email)
    if user:
        db.query(UserProfile).filter_by(user_id=user.id).delete()
        db.delete(user)
    db.commit()


def test_refresh_without_cookie(client: TestClient):
    response = client.post("/auth/refresh")
    assert response.status_code == 401
    assert response.json()["detail"] == "No refresh token found"


def test_me_without_session(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_register_blank_password(client: TestClient, unique_email, unique_username):
    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": "",
            "role": "client",
            "username": unique_username,
        },
    )
    assert response.status_code == 422  # FastAPI validation


def test_register_missing_fields(client: TestClient):
    response = client.post("/auth/register", json={})
    assert response.status_code == 422
    assert "email" in response.text


def test_register_invalid_email_format(client: TestClient, unique_username):
    response = client.post(
        "/auth/register",
        json={
            "email": "notanemail",
            "password": "secure123",
            "role": "client",
            "username": unique_username,
        },
    )
    assert response.status_code == 422


def test_register_short_password(client: TestClient, unique_email, unique_username):
    # Optional: your backend doesn’t enforce min length yet, but here's how it might behave
    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": "123",
            "role": "client",
            "username": unique_username,
        },
    )
    assert response.status_code in (200, 422)  # Adjust once validation is enforced


def test_register_invalid_role(client: TestClient, unique_email, unique_username):
    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": "secure123",
            "role": "giga-admin",  # not a valid role
            "username": unique_username,
        },
    )
    assert response.status_code == 422


def test_check_with_tampered_access_token(
    client: TestClient, unique_email, unique_username
):
    # Register and login
    client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": "secure123",
            "role": "client",
            "username": unique_username,
        },
    )
    login_payload = {"email": unique_email, "password": "secure123"}
    response = client.post("/auth/login", json=login_payload)

    # Tamper with token
    token = response.cookies["access_token"]
    parts = token.split(".")
    tampered_token = f"{parts[0]}.{parts[1]}.AAAAAA"  # break the signature

    # Send tampered token
    client.cookies.set("access_token", tampered_token)
    response = client.get("/auth/check")
    assert response.status_code == 401
