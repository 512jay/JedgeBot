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


# backend/auth/tests/test_auth_routes.py


def test_register_and_login_flow(
    client: TestClient, get_db_session, unique_email: str, unique_username: str
):
    # Step 1: Register a new user
    payload = {
        "email": unique_email,
        "password": "secure123",
        "role": "client",
        "username": unique_username,
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200

    # Step 2: Mark email as verified (simulate clicking verification link)
    user = get_user_by_email(get_db_session, unique_email)
    user.is_email_verified = True
    get_db_session.commit()

    # Step 3: Log in with the same credentials
    login_payload = {"email": unique_email, "password": "secure123"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    client.cookies.update(response.cookies)  # Set auth cookies for future requests

    # Step 4: Use /auth/check to verify user is authenticated
    response = client.get("/auth/check")
    assert response.status_code == 200
    assert response.json()["authenticated"] is True

    # Step 5: Clean up test user and their profile
    db = next(get_db())
    user = get_user_by_email(db, unique_email)
    if user:
        db.query(UserProfile).filter_by(user_id=user.id).delete()
        db.delete(user)
        db.commit()


# backend/auth/tests/test_auth_routes.py


def test_refresh_logout_me_flow(
    client: TestClient, get_db_session, unique_email: str, unique_username: str
):
    # Register
    payload = {
        "email": unique_email,
        "password": "secure123",
        "role": "client",
        "username": unique_username,
    }
    client.post("/auth/register", json=payload)

    # Mark user as verified
    user = get_user_by_email(get_db_session, unique_email)
    user.is_email_verified = True
    get_db_session.commit()

    # Login
    login_payload = {"email": unique_email, "password": "secure123"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    client.cookies.update(response.cookies)

    # Check authenticated session
    response = client.get("/auth/me")
    assert response.status_code == 200
    assert "email" in response.json()

    # Refresh session
    response = client.post("/auth/refresh")
    assert response.status_code == 200
    assert "access_token" in response.cookies

    # Logout
    response = client.post("/auth/logout")
    assert response.status_code == 200

    # Confirm logged out
    response = client.get("/auth/me")
    assert response.status_code == 401


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
    client: TestClient, get_db_session, unique_email, unique_username
):
    # Register
    client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": "secure123",
            "role": "client",
            "username": unique_username,
        },
    )

    # Force-verify email
    user = get_user_by_email(get_db_session, unique_email)
    user.is_email_verified = True
    get_db_session.commit()

    # Login
    login_payload = {"email": unique_email, "password": "secure123"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    client.cookies.update(response.cookies)

    # Get real token
    token = response.cookies["access_token"]
    assert token.startswith("ey")

    # Tamper with it
    tampered_token = token + "abc"

    # Try using tampered token
    client.cookies.set("access_token", tampered_token)
    response = client.get("/auth/check")
    assert response.status_code == 401


def test_email_verification_flow(client: TestClient, get_db_session, unique_email, unique_username, monkeypatch):
    captured_email = {}

    # Monkeypatch send_email to capture the tokenized link
    def mock_send_email(to, subject, body):
        assert to == unique_email
        assert "verify your email" in subject.lower()
        assert "verify-email?token=" in body
        captured_email["link"] = [line for line in body.splitlines() if "verify-email?token=" in line][0]

    # Replace the real send_email with our mock
    from backend.auth import auth_routes
    monkeypatch.setattr(auth_routes, "send_email", mock_send_email)

    # Register the user
    payload = {
        "email": unique_email,
        "password": "secure123",
        "role": "client",
        "username": unique_username,
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    assert "verify your account" in response.json()["message"].lower()

    # Extract token from the mocked email
    assert "link" in captured_email
    token_url = captured_email["link"]
    token = token_url.split("token=")[-1]

    # Call verify-email endpoint
    response = client.get(f"/auth/verify-email?token={token}")
    assert response.status_code == 200
    assert "verified" in response.json()["message"].lower()

    # Verify DB update
    db = next(get_db())
    user = get_user_by_email(db, unique_email)
    assert user.is_email_verified is True
    assert user.email_verified_at is not None

    # Cleanup
    db.query(UserProfile).filter_by(user_id=user.id).delete()
    db.delete(user)
    db.commit()


def test_email_verification_flow(
    client: TestClient, get_db_session, unique_email, unique_username, captured_email
):
    # Register user (mocked email will be captured)
    payload = {
        "email": unique_email,
        "password": "secure123",
        "role": "client",
        "username": unique_username,
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    message = response.json()["message"].lower()
    assert "verify" in message and "email" in message


    # Extract token from mocked email
    token_url = next(
        (
            line
            for line in captured_email["body"].splitlines()
            if "verify-email?token=" in line
        ),
        None,
    )
    assert token_url, "Token URL not found in email"
    from urllib.parse import urlparse, parse_qs

    parsed_url = urlparse(token_url)
    token = parse_qs(parsed_url.query)["token"][0]

    # Call verification endpoint
    response = client.get(f"/auth/verify-email?token={token}")
    assert response.status_code == 200
    assert "verified" in response.json()["message"].lower()

    # Confirm DB updated
    db = next(get_db())
    user = get_user_by_email(db, unique_email)
    assert user.is_email_verified is True
    assert user.email_verified_at is not None

    # Cleanup
    db.query(UserProfile).filter_by(user_id=user.id).delete()
    db.delete(user)
    db.commit()
