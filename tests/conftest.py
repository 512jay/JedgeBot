import pytest
from unittest.mock import MagicMock
from jedgebot.broker.tastytrade.api_client import APIClient
from jedgebot.broker.tastytrade.authentication import Authentication

@pytest.fixture
def mock_auth():
    """Fixture to mock authentication system returning a session token."""
    mock_auth = MagicMock(spec=Authentication)
    mock_auth.get_session_token.return_value = "mocked_token"
    return mock_auth

@pytest.fixture
def mock_api_client(mock_auth):
    """Fixture to mock API client, using mock authentication."""
    client = MagicMock(spec=APIClient)
    client.auth = mock_auth
    client.get.return_value = {}  # Default empty response
    return client

@pytest.fixture
def tastytrade_mock_accounts():
    """Mock response for the /customers/me/accounts API."""
    return {
        "data": {
            "items": [
                {"account": {"account-number": "5WT00001"}},
                {"account": {"account-number": "5WT00002"}}
            ]
        }
    }

@pytest.fixture
def tastytrade_mock_orders():
    """Mock response for fetching orders."""
    return {
        "data": {
            "items": [
                {"order-id": "O123", "symbol": "AAPL"},
                {"order-id": "O456", "symbol": "TSLA"}
            ]
        }
    }
