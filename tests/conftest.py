import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.core.settings import settings
from backend.data.database.auth.auth_db import get_db

# ✅ Assert the test mode is actually enabled
assert settings.TESTING is True, "TESTING must be true when running tests"

@pytest.fixture
def client():
    return TestClient(app)


# Optional: ensure DB schema is ready
from backend.data.database.auth.auth_db import init_db


@pytest.fixture(scope="session", autouse=True)
def setup_real_db():
    init_db()  # runs only once per test session
