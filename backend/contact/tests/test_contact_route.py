# /backend/contact/tests/test_contact_route.py
# Tests for /api/contact route with mocked email sending

from fastapi.testclient import TestClient
from unittest.mock import patch


def test_send_contact_message(client: TestClient):
    payload = {
        "email": "contacttest@example.com",
        "message": "This is a test message from the contact form.",
    }

    # Patch the send_email function where it's used
    with patch("backend.contact.routes.send_email") as mock_send:
        mock_send.return_value = None  # prevent real email
        response = client.post("/api/contact", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Your message has been sent successfully."
    mock_send.assert_called_once_with(
        to="admin@fordisludus.com",
        subject="Contact Form Submission from contacttest@example.com",
        body="This is a test message from the contact form.",
    )


def test_contact_missing_email(client: TestClient):
    payload = {"message": "Missing email field."}

    response = client.post("/api/contact", json=payload)
    assert (
        response.status_code == 422
    )  # Unprocessable Entity (Pydantic validation error)
    assert "email" in response.text


def test_contact_invalid_email_format(client: TestClient):
    payload = {"email": "not-an-email", "message": "Still trying to send something..."}

    response = client.post("/api/contact", json=payload)
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text


def test_contact_missing_message(client: TestClient):
    payload = {"email": "someone@example.com"}

    response = client.post("/api/contact", json=payload)
    assert response.status_code == 422
    assert "message" in response.text
