# /tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from backend.main import app
from backend.auth.auth_db import get_db
from backend.auth.auth_services import create_user, hash_password
from backend.auth.models import UserRole
from tests.utils.user_factory import random_email, random_password


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user(client):
    db = next(get_db())
    email = random_email()
    password = random_password()
    role = UserRole.CLIENT
    hashed = hash_password(password)

    # ✅ Pass hashed password as positional argument
    create_user(db, email, hashed, role)

    yield {"email": email, "password": password}

    # 🧼 Securely delete test user using parameterized query
    db.execute(text("DELETE FROM users WHERE email = :email"), {"email": email})
    db.commit()
