# /tests/integration/auth/test_password_reset.py

import uuid
import secrets
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.main import app
from backend.data.database.auth.auth_db import get_db
from backend.data.database.auth.auth_services import hash_password, create_user, verify_password
from backend.data.database.auth.models import User, UserRole
from backend.data.database.auth.password_reset_models import PasswordResetToken

client = TestClient(app)


def generate_unique_email() -> str:
    return f"reset_test_{uuid.uuid4().hex[:8]}@example.com"


def get_user_and_reset_tokens(
    db: Session, email: str
) -> tuple[User, list[PasswordResetToken]]:
    user = db.query(User).filter_by(email=email).first()
    assert user is not None, f"User not found for email: {email}"
    tokens = db.query(PasswordResetToken).filter_by(user_id=user.id).all()
    return user, tokens


def cleanup_user_and_tokens(db: Session, user: User) -> None:
    db.query(PasswordResetToken).filter_by(user_id=user.id).delete()
    db.delete(user)
    db.commit()


def test_forgot_password_creates_token_for_valid_email() -> None:
    email = generate_unique_email()
    password_hash = hash_password("resetpass123")
    db_gen = get_db()
    db: Session = next(db_gen)

    # Create user
    user = create_user(
        db, email=email, password_hash=password_hash, role=UserRole.CLIENT
    )

    # Make forgot-password request
    response = client.post("/auth/forgot-password", json={"email": email})
    assert response.status_code == 200
    assert "message" in response.json()

    # Check token exists
    _, tokens = get_user_and_reset_tokens(db, email)
    assert len(tokens) == 1
    assert tokens[0].used is False

    # Cleanup
    cleanup_user_and_tokens(db, user)
    try:
        next(db_gen)
    except StopIteration:
        pass

def test_forgot_password_with_invalid_email_returns_200_and_creates_no_token() -> None:
    email = "nonexistent_user@example.com"
    db_gen = get_db()
    db: Session = next(db_gen)

    # Pre-check: ensure user doesn't exist
    user = db.query(User).filter_by(email=email).first()
    assert user is None

    # Make request with invalid email
    response = client.post("/auth/forgot-password", json={"email": email})
    assert response.status_code == 200
    assert "message" in response.json()

    # Ensure no token was created
    tokens = db.query(PasswordResetToken).all()
    assert all(token.user_id != email for token in tokens)

    try:
        next(db_gen)
    except StopIteration:
        pass


def test_reset_password_with_valid_token_updates_password() -> None:
    from backend.data.database.auth.password_reset_service import (
        validate_password_reset_token,
    )

    email = generate_unique_email()
    old_password = "OldTestPass!456"
    new_password = "NewSecurePass!789"
    password_hash = hash_password(old_password)

    db_gen = get_db()
    db: Session = next(db_gen)

    # Step 1: Create user
    user = create_user(db, email=email, password_hash=password_hash)

    # Step 2: Generate reset token
    response = client.post("/auth/forgot-password", json={"email": email})
    assert response.status_code == 200

    # Step 3: Retrieve the token
    token_obj = (
        db.query(PasswordResetToken).filter_by(user_id=user.id, used=False).first()
    )
    assert token_obj is not None
    token = token_obj.token

    # Step 4: Submit new password
    reset_response = client.post(
        "/auth/reset-password", json={"token": token, "new_password": new_password}
    )
    assert reset_response.status_code == 200
    assert "Password reset successfully" in reset_response.json()["message"]

    # Step 5: Confirm token marked used
    db.refresh(token_obj)
    assert token_obj.used is True

    # Step 6: Confirm new password was saved
    db.expire_all()
    refreshed_user = db.query(User).filter_by(id=user.id).first()
    assert refreshed_user is not None
    assert verify_password(new_password, refreshed_user.password_hash)

    # Cleanup
    db.delete(refreshed_user)
    db.commit()
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_reset_password_with_invalid_token_returns_400() -> None:
    db_gen = get_db()
    db: Session = next(db_gen)

    invalid_token = secrets.token_urlsafe(16)  # Generate a random token    
    new_password = "DoesNotMatter123"

    # Attempt to reset with invalid token
    response = client.post(
        "/auth/reset-password",
        json={"token": invalid_token, "new_password": new_password},
    )

    assert response.status_code == 400
    assert "Invalid or unknown token" in response.json()["detail"]

    try:
        next(db_gen)
    except StopIteration:
        pass


def test_reset_password_with_used_token_returns_400() -> None:
    email = generate_unique_email()
    db_gen = get_db()
    db: Session = next(db_gen)

    user = create_user(db, email=email, password_hash=hash_password("initial123"))

    # Generate reset token
    client.post("/auth/forgot-password", json={"email": email})
    token_obj = (
        db.query(PasswordResetToken).filter_by(user_id=user.id, used=False).first()
    )
    assert token_obj is not None
    token = token_obj.token

    # Use the token once
    client.post(
        "/auth/reset-password", json={"token": token, "new_password": "newpass123"}
    )

    # Try using the same token again
    response = client.post(
        "/auth/reset-password", json={"token": token, "new_password": "failpass456"}
    )
    assert response.status_code == 400
    assert "already been used" in response.json()["detail"]

    # Cleanup
    db.query(PasswordResetToken).filter_by(user_id=user.id).delete()
    db.delete(user)
    db.commit()
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_reset_password_with_expired_token_returns_400() -> None:
    from datetime import datetime, timedelta

    email = generate_unique_email()
    db_gen = get_db()
    db: Session = next(db_gen)

    user = create_user(db, email=email, password_hash=hash_password("initial123"))

    import secrets
    token = secrets.token_urlsafe(16)

    expired_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() - timedelta(minutes=1),
        used=False,
    )
    db.add(expired_token)
    db.commit()

    # Use that same token in the request
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
