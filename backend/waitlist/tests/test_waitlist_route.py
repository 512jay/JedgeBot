# /backend/waitlist/tests/test_waitlist_route.py
# Unit tests for waitlist API route, mocking real email sending.
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.waitlist.models import WaitlistEntry


def test_submit_waitlist_entry(client: TestClient, get_db_session):
    payload = {
        "email": "testuser@example.com",
        "name": "Test User",
        "role": "trader",
        "feedback": "Excited to try the app!",
    }

    # Clean up if test email already exists
    existing = (
        get_db_session.query(WaitlistEntry).filter_by(email=payload["email"]).first()
    )
    if existing:
        get_db_session.delete(existing)
        get_db_session.commit()

    # ✅ Patch where it's used, not where it's defined
    with patch("backend.waitlist.routes.send_email") as mock_send:
        mock_send.return_value = None
        response = client.post("/api/waitlist", json=payload)

    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]
    mock_send.assert_called_once()


def test_waitlist_duplicate_entry(client: TestClient, get_db_session):
    payload = {
        "email": "duplicate@example.com",
        "name": "Already Exists",
        "role": "trader",
        "feedback": None,
    }

    with patch("backend.notifications.smtp_service.send_email") as mock_send:
        mock_send.return_value = None
        client.post("/api/waitlist", json=payload)

    response = client.post("/api/waitlist", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "This email is already on the waitlist."
