import pytest
from unittest.mock import MagicMock
from jedgebot.broker.tastytrade.services.customer_service import CustomerService
from jedgebot.broker.tastytrade.api_client import APIClient

@pytest.fixture
def mock_api_client():
    """Fixture to create a mock APIClient instance."""
    return MagicMock(spec=APIClient)

@pytest.fixture
def customer_service(mock_api_client):
    """Fixture to create a CustomerService instance with a mocked API client."""
    return CustomerService(mock_api_client)

def test_get_customer_info(customer_service, mock_api_client):
    """Test retrieving customer information."""
    mock_api_client.get.return_value = {"data": {"name": "Test User", "email": "test@example.com"}}

    result = customer_service.get_customer_info()

    assert result == {"name": "Test User", "email": "test@example.com"}
    mock_api_client.get.assert_called_once_with("/customers/me")

def test_get_customer_accounts(customer_service, mock_api_client):
    """Test retrieving customer accounts."""
    mock_api_client.get.return_value = {
        "data": {
            "items": [
                {"account": {"account-number": "5WT00001"}},
                {"account": {"account-number": "5WT00002"}}
            ]
        }
    }

    result = customer_service.get_customer_accounts()

    assert result == [
        {"account": {"account-number": "5WT00001"}},
        {"account": {"account-number": "5WT00002"}}
    ]
    mock_api_client.get.assert_called_once_with("/customers/me/accounts")
