# /backend/waitlist/tests/test_waitlist_route.py

import pytest
from httpx import AsyncClient
from backend.main import app
from backend.data.database.db import get_db
from backend.waitlist.models import WaitlistEntry
from fastapi.testclient import TestClient  # add this


def test_submit_waitlist_entry(client: TestClient, get_db_session):
    payload = {
        "email": "testuser@example.com",
        "name": "Test User",
        "role": "trader",
        "feedback": "Excited to try the app!",
    }

    # 🚨 Clean up if test email already exists
    existing = (
        get_db_session.query(WaitlistEntry).filter_by(email=payload["email"]).first()
    )
    if existing:
        get_db_session.delete(existing)
        get_db_session.commit()

    # First submission: should succeed
    response = client.post("/api/waitlist", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == payload["email"]
    assert data["role"] == payload["role"]
    assert "submitted_at" in data

    entry = (
        get_db_session.query(WaitlistEntry).filter_by(email=payload["email"]).first()
    )
    assert entry is not None
    assert entry.role.value == "trader"  # or UserRole.trader

    # Duplicate submission: should fail
    duplicate = client.post("/api/waitlist", json=payload)
    assert duplicate.status_code == 409
