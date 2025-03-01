import pytest
import requests
from unittest.mock import patch, MagicMock
from jedgebot.api.request_utils import request_with_retry

def test_request_with_retry_success():
    """Test that request_with_retry succeeds on the first attempt."""
    with patch("requests.request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"success": True}

        response = request_with_retry("http://fakeurl.com")
        assert response == {"success": True}

def test_request_with_retry_fails_then_succeeds():
    """Test that request_with_retry retries on failure and eventually succeeds."""
    
    # Create a mock response with status_code 200
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = {"success": True}

    with patch("requests.request") as mock_request:
        mock_request.side_effect = [
            requests.exceptions.RequestException("Failed"),
            requests.exceptions.RequestException("Failed"),
            success_response  # ✅ Properly mocked successful response
        ]

        response = request_with_retry("http://fakeurl.com")
        assert response == {"success": True}
