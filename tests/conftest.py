# /tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app  # make sure this is your FastAPI app import


@pytest.fixture
def client():
    return TestClient(app)
