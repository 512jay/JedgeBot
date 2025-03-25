# /tests/unit/auth/test_auth_routes.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import UUID
import uuid

from backend.main import app
from backend.data.database.auth.auth_db import get_db
from backend.data.database.auth.models import User, UserRole

client = TestClient(app)


def test_register_user_with_manager_role() -> None:
    # Step 1: Register with unique email
    test_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": test_email, "password": "strongpassword123", "role": "manager"}

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200, response.text
    assert "manager" in response.json()["message"]

    # Step 2: Confirm user exists in the DB
    db_gen = get_db()
    db: Session = next(db_gen)
    user: User | None = db.query(User).filter_by(email=test_email).first()

    assert user is not None
    assert user.role == UserRole.MANAGER

    # Step 3: Clean up test user
    db.delete(user)
    db.commit()

    try:
        next(db_gen)
    except StopIteration:
        pass


def test_auth_me_route(client, test_user):
    response = client.post("/auth/login", json=test_user)
    assert response.status_code == 200
    cookies = response.cookies

    client.cookies = cookies
    me_response = client.get("/auth/me")
    assert me_response.status_code == 200
    data = me_response.json()
    assert data["email"] == test_user["email"]
    assert "role" in data
