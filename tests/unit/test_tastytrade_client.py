import pytest
from unittest.mock import MagicMock, patch
from jedgebot.broker.tastytrade.tastytrade_client import TastyTradeClient
from jedgebot.broker.tastytrade.authentication import Authentication
from jedgebot.broker.tastytrade.api_client import APIClient
from jedgebot.broker.tastytrade.services.account_service import AccountService
from jedgebot.broker.tastytrade.services.customer_service import CustomerService
from jedgebot.broker.tastytrade.services.order_service import OrderService
from jedgebot.broker.tastytrade.services.market_data_service import MarketDataService


@pytest.fixture
def mock_authentication():
    """Fixture to create a mocked authentication instance."""
    mock_auth = MagicMock(spec=Authentication)
    mock_auth.get_session_token.return_value = "mocked_token"
    return mock_auth


@pytest.fixture
def mock_api_client(mock_authentication):
    """Fixture to create a mocked API client."""
    return MagicMock(spec=APIClient)


@pytest.fixture
def mock_services(mock_api_client):
    """Fixture to create mocked service classes."""
    return {
        "account_service": MagicMock(spec=AccountService),
        "customer_service": MagicMock(spec=CustomerService),
        "order_service": MagicMock(spec=OrderService),
        "market_data_service": MagicMock(spec=MarketDataService),
    }


@pytest.fixture
def tastytrade_client(mock_authentication, mock_api_client, mock_services):
    """Fixture to create a TastyTradeClient instance with mocked dependencies."""
    with patch("jedgebot.broker.tastytrade.authentication.Authentication", return_value=mock_authentication), \
         patch("jedgebot.broker.tastytrade.api_client.APIClient", return_value=mock_api_client), \
         patch("jedgebot.broker.tastytrade.services.account_service.AccountService", return_value=mock_services["account_service"]), \
         patch("jedgebot.broker.tastytrade.services.customer_service.CustomerService", return_value=mock_services["customer_service"]), \
         patch("jedgebot.broker.tastytrade.services.order_service.OrderService", return_value=mock_services["order_service"]), \
         patch("jedgebot.broker.tastytrade.services.market_data_service.MarketDataService", return_value=mock_services["market_data_service"]):

        return TastyTradeClient("test_user", "test_pass")


def test_refresh_authentication(tastytrade_client, mock_authentication):
    """Test refreshing authentication tokens."""
    tastytrade_client.refresh_authentication()
    mock_authentication.ensure_authenticated.assert_called_once()


def test_get_accounts(tastytrade_client, mock_services):
    """Test retrieving accounts."""
    mock_services["account_service"].get_accounts.return_value = [{"account-number": "12345"}]
    accounts = tastytrade_client.get_accounts()
    assert accounts == [{"account-number": "12345"}]
    mock_services["account_service"].get_accounts.assert_called_once()


def test_place_order(tastytrade_client, mock_services):
    """Test placing an order."""
    mock_services["order_service"].place_order.return_value = {"status": "success"}
    result = tastytrade_client.place_order("12345", {"symbol": "AAPL"})
    assert result == {"status": "success"}
    mock_services["order_service"].place_order.assert_called_once_with("12345", {"symbol": "AAPL"})
