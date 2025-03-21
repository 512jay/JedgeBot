from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_register_user_with_role():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "secure123", "role": "client"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "client" in data["message"]
