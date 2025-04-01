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

    # Patch SMTP to avoid real email sending
    with patch("backend.notifications.email_service.smtplib.SMTP"):
        response = client.post("/api/waitlist", json=payload)

    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]


def test_waitlist_duplicate_entry(client: TestClient, get_db_session):
    payload = {
        "email": "duplicate@example.com",
        "name": "Already Exists",
        "role": "trader",
        "feedback": None,
    }

    # Insert first time
    with patch("backend.notifications.email_service.smtplib.SMTP"):
        client.post("/api/waitlist", json=payload)

    # Attempt duplicate
    response = client.post("/api/waitlist", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "This email is already on the waitlist."
