import os
from unittest.mock import patch

import pytest
import requests

from jedgebot.broker.tastytrade_broker import TastyTradeBroker


@pytest.fixture
def broker():
    """Fixture to initialize the broker with dry run mode."""
    os.environ["TASTYTRADE_DRY_RUN"] = "true"  # Ensure dry run is enabled
    return TastyTradeBroker()


def test_dry_run_place_order(broker):
    """Test that place_order does not execute real trades in dry run mode."""
    order_details = {
        "symbol": "AAPL",
        "quantity": 1,
        "order_type": "limit",  # Use limit order
        "price": 1.00,  # Unrealistic price to avoid accidental trades
    }

    result = broker.place_order(**order_details)
    print(f"Dry run place order result: {result}")

    assert result["status"] == "simulated"
    assert result["order"]["symbol"] == "AAPL"
    assert result["order"]["quantity"] == 1
    assert result["order"]["order_type"] == "limit"
    assert result["order"]["price"] == 1.00


def test_live_mode_place_order():
    """Test that place_order calls the real API when dry run is disabled, using a limit order."""
    os.environ["TASTYTRADE_DRY_RUN"] = "false"  # Ensure live mode is set
    broker = TastyTradeBroker()  # Reinitialize the broker to apply new env variables

    order_details = {
        "symbol": "AAPL",
        "quantity": 1,
        "order_type": "limit",  # Use a limit order instead of market
        "price": 1.00,  # Unrealistic price ensures no accidental fill
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"status": "success"}

        result = broker.place_order(**order_details)
        print(f"Live mode place order result: {result}")

        mock_post.assert_called_once()  # Ensure API was called
        assert result["status"] == "success"

    # Reset environment variable
    os.environ["TASTYTRADE_DRY_RUN"] = "true"


def test_authentication_failure():
    """Test that authentication fails gracefully with invalid credentials."""
    os.environ["TASTYTRADE_USERNAME"] = "invalid_user"
    os.environ["TASTYTRADE_PASSWORD"] = "wrong_password"

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 401
        mock_post.return_value.json.return_value = {
            "error": {"message": "Unauthorized"}
        }
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "401 Client Error: Unauthorized"
        )

        with pytest.raises(requests.exceptions.HTTPError):
            TastyTradeBroker()  # This should now raise the expected error


def test_place_order_success():
    """Test that place_order correctly sends a request and processes the response."""
    os.environ["TASTYTRADE_DRY_RUN"] = "false"  # Ensure dry run is disabled
    broker = TastyTradeBroker()

    order_details = {
        "symbol": "AAPL",
        "quantity": 1,
        "order_type": "limit",
        "price": 150.00,
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"status": "success"}

        result = broker.place_order(**order_details)
        print(f"Place order success result: {result}")

        mock_post.assert_called_once()  # ✅ Ensure API was called
        assert result["status"] == "success"

    # Reset dry run mode
    os.environ["TASTYTRADE_DRY_RUN"] = "true"


def test_place_order_failure():
    """Test that place_order raises an error when the API returns a failure."""
    broker = TastyTradeBroker()

    order_details = {
        "symbol": "AAPL",
        "quantity": 1,
        "order_type": "limit",
        "price": 150.00,
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"error": "Invalid order"}
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "400 Client Error: Bad Request"
        )

        with pytest.raises(requests.exceptions.HTTPError):
            broker.place_order(**order_details)


def test_get_account_balance():
    """Test fetching account balance."""
    broker = TastyTradeBroker()

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"balance": 5000.00}

        result = broker.get_account_balance()
        print(f"Get account balance result: {result}")

        mock_get.assert_called_once()
        assert result["balance"] == 5000.00


def test_cancel_order():
    """Test canceling an order successfully."""
    broker = TastyTradeBroker()
    order_id = "12345"

    with patch("requests.delete") as mock_delete:
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {"status": "Order canceled"}

        result = broker.cancel_order(order_id)
        print(f"Cancel order result: {result}")

        mock_delete.assert_called_once()
        assert result["status"] == "Order canceled"  # ✅ Match actual return value


def test_get_market_data():
    """Test fetching market data for a stock."""
    broker = TastyTradeBroker()
    symbol = "AAPL"

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"price": 150.25}

        result = broker.get_market_data(symbol)
        print(f"Get market data result: {result}")

        mock_get.assert_called_once()
        assert result["price"] == 150.25


def test_get_buying_power():
    """Test fetching buying power."""
    broker = TastyTradeBroker()

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"buying_power": 10000.00}

        result = broker.get_buying_power()
        print(f"Get buying power result: {result}")

        mock_get.assert_called_once()
        assert result["buying_power"] == 10000.00
