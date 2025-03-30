# /tests/unit/auth/test_dependencies.py
# Unit tests for backend.auth.dependencies.get_current_user

import pytest
from fastapi import Request, HTTPException
from starlette.requests import Request as StarletteRequest
from jose import jwt
from datetime import datetime, timedelta
import os
from backend.auth.dependencies import get_current_user

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_test_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


class DummyRequest(StarletteRequest):
    def __init__(self, token: str):
        scope = {
            "type": "http",
            "headers": [(b"cookie", f"access_token={token}".encode())],
        }
        super().__init__(scope)


def test_get_current_user_valid_token():
    token = create_test_token("test@example.com")
    request = DummyRequest(token)
    user = get_current_user(request)
    assert user["email"] == "test@example.com"


def test_get_current_user_missing_token():
    scope = {"type": "http", "headers": []}
    request = StarletteRequest(scope)
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(request)
    assert exc_info.value.status_code == 401


def test_get_current_user_invalid_token():
    request = DummyRequest("invalid.token.here")
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(request)
    assert exc_info.value.status_code == 401
