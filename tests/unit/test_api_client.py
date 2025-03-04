import pytest
import requests
from unittest.mock import patch, MagicMock
from jedgebot.broker.tastytrade.api_client import APIClient
from jedgebot.broker.tastytrade.authentication import Authentication

@pytest.fixture
def mock_authentication():
    """Fixture to create a mock authentication instance."""
    mock_auth = MagicMock(spec=Authentication)
    mock_auth.get_session_token.return_value = "mocked_token"
    return mock_auth

@pytest.fixture
def api_client(mock_authentication):
    """Fixture to create an APIClient instance with mocked authentication."""
    return APIClient(mock_authentication)

@pytest.fixture
def mock_requests():
    """Fixture to patch individual HTTP methods of requests."""
    with patch("requests.get") as mock_get, patch("requests.post") as mock_post, patch("requests.put") as mock_put, patch("requests.delete") as mock_delete:
        yield {
            "GET": mock_get,
            "POST": mock_post,
            "PUT": mock_put,
            "DELETE": mock_delete
        }

@pytest.mark.parametrize("method, endpoint, status_code, response_data", [
    ("GET", "/test-get", 200, {"message": "GET success"}),
    ("POST", "/test-post", 201, {"message": "POST success"}),
    ("PUT", "/test-put", 200, {"message": "PUT success"}),
    ("DELETE", "/test-delete", 204, None),
])
def test_api_client_methods(api_client, mock_requests, method, endpoint, status_code, response_data):
    """Test all HTTP methods of APIClient with a mocked response."""
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = response_data

    # Get the correct mock method based on HTTP method
    mock_requests[method].return_value = mock_response

    if method == "GET":
        result = api_client.get(endpoint)
    elif method == "POST":
        result = api_client.post(endpoint, data={"key": "value"})
    elif method == "PUT":
        result = api_client.put(endpoint, data={"key": "value"})
    elif method == "DELETE":
        result = api_client.delete(endpoint)
        assert result is None
        return

    assert result == response_data

    # Fixing the assertion differences
    expected_call_kwargs = {
        "headers": {"Authorization": "mocked_token", "Content-Type": "application/json"},
    }

    if method == "GET":
        expected_call_kwargs["params"] = None  # Ensure compatibility with how requests is called
    elif method in ["POST", "PUT"]:
        expected_call_kwargs["json"] = {"key": "value"}

    mock_requests[method].assert_called_once_with(
        f"https://api.tastytrade.com{endpoint}",
        **expected_call_kwargs
    )

def test_api_client_handles_errors(api_client, mock_requests):
    """Test APIClient error handling for a failed request."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Bad Request"}
    mock_response.raise_for_status.side_effect = requests.HTTPError("400 Client Error: Bad Request")

    # Fix incorrect return value assignment
    mock_requests["GET"].return_value = mock_response

    with pytest.raises(requests.HTTPError):
        api_client.get("/test-error")

    mock_requests["GET"].assert_called_once()
