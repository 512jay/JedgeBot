# /tests/unit/test_auth_routes.py

from fastapi.testclient import TestClient
from backend.main import app
from backend.data.database.auth.auth_db import get_db
from backend.data.database.auth.models import User
from sqlalchemy.orm import Session
import uuid

client = TestClient(app)


def test_register_user_with_role(client: TestClient) -> None:
    test_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": test_email, "password": "testpassword123", "role": "manager"}

    # Register new user
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200, response.text
    assert "manager" in response.json()["message"]

    # Verify user in DB
    db: Session = next(get_db())
    user: User | None = db.query(User).filter_by(email=test_email).first()
    assert user is not None
    assert user.role.value == "manager"

    # Cleanup test user
    db.delete(user)
    db.commit()
