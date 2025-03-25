# /tests/integration/auth/test_validate_token.py

import uuid
import secrets
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.main import app
from backend.auth.auth_db import get_db
from backend.auth.auth_services import create_user, hash_password
from backend.auth.password_reset_models import PasswordResetToken

client = TestClient(app)


def generate_email() -> str:
    return f"token_test_{uuid.uuid4().hex[:8]}@example.com"


def test_validate_token_with_valid_token() -> None:
    email = generate_email()
    db_gen = get_db()
    db: Session = next(db_gen)

    user = create_user(db, email=email, password_hash=hash_password("Test1234"))

    token_value = secrets.token_urlsafe(30)

    token = PasswordResetToken(
        user_id=user.id,
        token=token_value,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
        used=False,
    )
    db.add(token)
    db.commit()

    response = client.get("/auth/validate-token", params={"token": token_value})
    assert response.status_code == 200
    assert "Token is valid" in response.json()["message"]

    # ✅ Clean up safely
    db.query(PasswordResetToken).filter_by(user_id=user.id).delete()
    db.delete(user)
    db.commit()
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_reset_password_with_expired_token_returns_400() -> None:
    from datetime import datetime, timedelta

    email = generate_email()
    db_gen = get_db()
    db: Session = next(db_gen)

    user = create_user(db, email=email, password_hash=hash_password("initial123"))

    # Use a random token string to avoid UNIQUE violation
    import secrets

    token = secrets.token_urlsafe(32)

    expired_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() - timedelta(minutes=1),
        used=False,
    )
    db.add(expired_token)
    db.commit()

    # Attempt to reset password with expired token
    response = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "fail123"},
    )
    assert response.status_code == 400
    assert "expired" in response.json()["detail"]

    # Cleanup
    db.query(PasswordResetToken).filter_by(user_id=user.id).delete()
    db.delete(user)
    db.commit()
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_validate_token_with_nonexistent_token_returns_400() -> None:
    response = client.get(
        "/auth/validate-token", params={"token": "this-token-does-not-exist"}
    )
    assert response.status_code == 400
    assert "Invalid or unknown token" in response.json()["detail"]
