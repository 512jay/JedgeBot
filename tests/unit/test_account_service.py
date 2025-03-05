import pytest
from unittest.mock import MagicMock
from jedgebot.broker.tastytrade.services.account import AccountService
from jedgebot.broker.tastytrade.api_client import APIClient

@pytest.fixture
def mock_api_client():
    """Fixture to create a mock APIClient instance."""
    return MagicMock(spec=APIClient)

@pytest.fixture
def account_service(mock_api_client):
    """Fixture to create an AccountService instance with a mocked APIClient."""
    return AccountService(mock_api_client)

def test_get_accounts(account_service, mock_api_client):
    """Test retrieving a list of account numbers."""
    mock_response = {
        "data": {
            "items": [
                {"account": {"account-number": "5WT00001"}},
                {"account": {"account-number": "5WT00002"}}
            ]
        }
    }
    mock_api_client.get.return_value = mock_response
    accounts = account_service.get_accounts()
    assert accounts == ["5WT00001", "5WT00002"]
    mock_api_client.get.assert_called_once_with("/customers/me/accounts")

def test_get_account_details(account_service, mock_api_client):
    """Test retrieving details for a specific account."""
    account_number = "5WT00001"
    mock_response = {"data": {"account-number": account_number, "type": "Individual"}}
    mock_api_client.get.return_value = mock_response
    account_details = account_service.get_account_details(account_number)
    assert account_details == {"account-number": account_number, "type": "Individual"}
    mock_api_client.get.assert_called_once_with(f"/accounts/{account_number}")

def test_get_account_balances(account_service, mock_api_client):
    """Test retrieving balance details for an account."""
    account_number = "5WT00001"
    mock_response = {"data": {"cash-balance": 5000.00}}
    mock_api_client.get.return_value = mock_response
    balances = account_service.get_account_balances(account_number)
    assert balances == {"cash-balance": 5000.00}
    mock_api_client.get.assert_called_once_with(f"/accounts/{account_number}/balances")

def test_get_account_positions(account_service, mock_api_client):
    """Test retrieving positions for an account."""
    account_number = "5WT00001"
    mock_response = {"data": [{"symbol": "AAPL", "quantity": 10}, {"symbol": "TSLA", "quantity": 5}]}
    mock_api_client.get.return_value = mock_response
    positions = account_service.get_account_positions(account_number)
    assert positions == [{"symbol": "AAPL", "quantity": 10}, {"symbol": "TSLA", "quantity": 5}]
    mock_api_client.get.assert_called_once_with(f"/accounts/{account_number}/positions")

def test_get_account_orders(account_service, mock_api_client):
    """Test retrieving all orders for an account."""
    account_number = "5WT00001"
    mock_response = {"data": [{"order-id": "12345"}, {"order-id": "67890"}]}
    mock_api_client.get.return_value = mock_response
    orders = account_service.get_account_orders(account_number)
    assert orders == [{"order-id": "12345"}, {"order-id": "67890"}]
    mock_api_client.get.assert_called_once_with(f"/accounts/{account_number}/orders")
