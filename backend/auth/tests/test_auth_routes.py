# /backend/auth/tests/test_auth_routes.py
# Integration tests for auth endpoints using TestClient and real DB.

import uuid
import pytest
from fastapi.testclient import TestClient
from backend.auth.auth_models import UserRole
from backend.data.database.db import get_db
from backend.auth.auth_queries import get_user_by_email


@pytest.fixture
def unique_email():
    return f"testuser_{uuid.uuid4()}@example.com"


def test_register_and_login_flow(client: TestClient, get_db_session, unique_email: str):
    # -------------------------
    # Register
    # -------------------------
    payload = {
        "email": unique_email,
        "password": "secure123",
        "role": "client",
        "username": "route_tester",
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 200
    assert "User registered successfully" in response.json()["message"]

    # -------------------------
    # Login
    # -------------------------
    login_payload = {"email": unique_email, "password": "secure123"}
    response = client.post("/login", json=login_payload)
    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert response.json()["user"]["email"] == unique_email
    assert response.json()["user"]["role"] == "client"

    # -------------------------
    # Check auth status
    # -------------------------
    response = client.get("/check", cookies=response.cookies)
    assert response.status_code == 200
    assert response.json()["authenticated"] is True
    assert response.json()["email"] == unique_email
    assert response.json()["role"] == "client"

    # Cleanup
    db = next(get_db())
    user = get_user_by_email(db, unique_email)
    db.delete(user)
    db.commit()
