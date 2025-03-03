import os
import re
import json
import pytest
import requests
from jedgebot.broker.tastytrade_broker import TastyTradeBroker

@pytest.fixture
def broker():
    """Fixture to initialize the broker with dry run mode enabled."""
    os.environ["TASTYTRADE_DRY_RUN"] = "true"
    broker_instance = TastyTradeBroker()
    broker_instance.token = "mock_token"  # Set a mock token
    return broker_instance


@pytest.fixture
def live_broker():
    """Fixture to initialize the broker with dry run mode disabled."""
    os.environ["TASTYTRADE_DRY_RUN"] = "false"
    broker_instance = TastyTradeBroker()
    broker_instance.token = "mock_token"  # Set a mock token
    return broker_instance

@pytest.fixture
def temp_remember_me_file(tmp_path):
    """Fixture to provide a temporary remember-me file."""
    return tmp_path / "remember_me.json"

def test_get_open_orders_success(mocker, live_broker):
    """Test successful retrieval of open orders."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"orders": [{"id": "123", "status": "open"}]}
    mock_response.raise_for_status = lambda: None  # No exception raised

    mocker.patch("requests.get", return_value=mock_response)

    result = live_broker.get_open_orders()

    assert "orders" in result
    assert result["orders"][0]["status"] == "open"

def test_get_order_status_success(mocker, live_broker):
    """Test successful retrieval of order status."""
    order_id = "12345"
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"id": order_id, "status": "filled"}
    mock_response.raise_for_status = lambda: None  # No exception raised

    mocker.patch("requests.get", return_value=mock_response)

    result = live_broker.get_order_status(order_id)

    assert result["status"] == "filled"

def test_stream_market_data_success(mocker, live_broker):
    """Test real-time market data streaming."""
    mock_response = mocker.MagicMock()
    mock_response.iter_lines.return_value = [
        json.dumps({"symbol": "AAPL", "price": 150.0}).encode("utf-8")
    ]
    mock_response.raise_for_status = lambda: None  # No exception raised

    # Ensuring `requests.get` works as a context manager
    mock_get = mocker.patch("requests.get", return_value=mock_response)
    mock_get.return_value.__enter__.return_value = mock_response

    callback_called = []

    def callback(data):
        callback_called.append(data)

    live_broker.stream_market_data(["AAPL"], callback)

    assert callback_called == [{"symbol": "AAPL", "price": 150.0}]

def test_stream_market_data_failure(mocker, live_broker):
    """Test failure when streaming market data."""
    mock_response = mocker.MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("503 Service Unavailable")

    # Ensuring `requests.get` works as a context manager
    mock_get = mocker.patch("requests.get", return_value=mock_response)
    mock_get.return_value.__enter__.return_value = mock_response

    callback_called = []

    def callback(data):
        callback_called.append(data)

    with pytest.raises(requests.exceptions.HTTPError):
        live_broker.stream_market_data(["AAPL"], callback)

    assert callback_called == []

def test_get_market_data_success(mocker, live_broker):
    """Test successful retrieval of market data."""
    symbol = "AAPL"

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"price": 150.25}
    mock_response.raise_for_status = mocker.Mock()  # No exception raised

    # Patch requests.get to return mock response
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    result = live_broker.get_market_data(symbol)

    # Ensure requests.get was called with correct parameters
    mock_get.assert_called_once_with(
        f"{live_broker.BASE_URL}/market-data/{symbol}",
        headers={"Authorization": f"Bearer {live_broker.token}"},
    )

    # Verify the returned market data
    assert result["price"] == 150.25

def test_get_market_data_failure(mocker, live_broker):
    """Test API failure when retrieving market data."""
    symbol = "AAPL"

    mock_response = mocker.Mock()
    mock_response.status_code = 500  # Internal Server Error
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")

    # Patch requests.get to return mock response
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        live_broker.get_market_data(symbol)

    # Ensure requests.get was called
    mock_get.assert_called_once()

def test_get_trade_history_success(mocker, live_broker):
    """Test successful retrieval of trade history."""
    start_date = "2024-01-01"
    end_date = "2024-02-01"

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"trades": [{"symbol": "AAPL", "quantity": 10, "price": 145.00}]}
    mock_response.raise_for_status = mocker.Mock()

    # Patch requests.get to return mock response
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    result = live_broker.get_trade_history(start_date, end_date)

    # Ensure requests.get was called with correct parameters
    mock_get.assert_called_once_with(
        f"{live_broker.BASE_URL}/trade-history?start={start_date}&end={end_date}",
        headers={"Authorization": f"Bearer {live_broker.token}"},
    )

    # Verify trade history data
    assert result["trades"][0]["symbol"] == "AAPL"
    assert result["trades"][0]["quantity"] == 10
    assert result["trades"][0]["price"] == 145.00

def test_get_trade_history_failure(mocker, live_broker):
    """Test API failure when retrieving trade history."""
    start_date = "2024-01-01"
    end_date = "2024-02-01"

    mock_response = mocker.Mock()
    mock_response.status_code = 403  # Unauthorized
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Forbidden")

    # Patch requests.get to return mock response
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        live_broker.get_trade_history(start_date, end_date)

    # Ensure requests.get was called
    mock_get.assert_called_once()

def test_get_buying_power_success(mocker, live_broker):
    """Test successful retrieval of buying power."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"buying_power": 10000.00}
    mock_response.raise_for_status = mocker.Mock()

    # Patch requests.get to return mock response
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    result = live_broker.get_buying_power()

    # Ensure requests.get was called with correct parameters
    mock_get.assert_called_once_with(
        f"{live_broker.BASE_URL}/accounts/buying-power",
        headers={"Authorization": f"Bearer {live_broker.token}"},
    )

    # Verify buying power
    assert result["buying_power"] == 10000.00

def test_get_buying_power_failure(mocker, live_broker):
    """Test API failure when retrieving buying power."""
    mock_response = mocker.Mock()
    mock_response.status_code = 400  # Bad Request
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("400 Bad Request")

    # Patch requests.get to return mock response
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        live_broker.get_buying_power()

    # Ensure requests.get was called
    mock_get.assert_called_once()

def test_cancel_order_success(mocker, live_broker):
    """Test successful cancellation of an order."""
    order_id = "12345"

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status = mocker.Mock()  # No exception raised

    # Patch requests.delete to return mock response
    mock_delete = mocker.patch("requests.delete", return_value=mock_response)

    result = live_broker.cancel_order(order_id)

    # Ensure requests.delete was called with the correct parameters
    mock_delete.assert_called_once_with(
        f"{live_broker.BASE_URL}/orders/{order_id}",
        headers={"Authorization": f"Bearer {live_broker.token}"},
    )

    # Verify the returned response
    assert result == {"status": "Order canceled"}

def test_cancel_order_failure(mocker, live_broker):
    """Test API failure when canceling an order."""
    order_id = "12345"

    mock_response = mocker.Mock()
    mock_response.status_code = 404  # Order not found
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")

    # Patch requests.delete to return mock response
    mock_delete = mocker.patch("requests.delete", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        live_broker.cancel_order(order_id)

    # Ensure requests.delete was called
    mock_delete.assert_called_once_with(
        f"{live_broker.BASE_URL}/orders/{order_id}",
        headers={"Authorization": f"Bearer {live_broker.token}"},
    )

def test_get_account_balance_success(mocker, live_broker):
    """Test successful retrieval of account balance."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"balance": 5000.00}
    mock_response.raise_for_status = mocker.Mock()  # No exception raised

    # Patch requests.get to return mock response
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    result = live_broker.get_account_balance()

    # Ensure requests.get was called with the correct parameters
    mock_get.assert_called_once_with(
        f"{live_broker.BASE_URL}/accounts",
        headers={"Authorization": f"Bearer {live_broker.token}"},
    )

    # Verify the returned balance is correct
    assert result["balance"] == 5000.00

def test_get_account_balance_failure(mocker, live_broker):
    """Test API failure when retrieving account balance."""
    mock_response = mocker.Mock()
    mock_response.status_code = 500  # Internal Server Error
    mock_response.json.return_value = {"error": "Server error"}
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")

    # Patch requests.get to return mock response
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        live_broker.get_account_balance()

    # Ensure requests.get was called
    mock_get.assert_called_once_with(
        f"{live_broker.BASE_URL}/accounts",
        headers={"Authorization": f"Bearer {live_broker.token}"},
    )

def test_authenticate_success(mocker, live_broker):
    """Test successful authentication where a session token is returned."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"session-token": "test_token"}}
    mock_response.raise_for_status = mocker.Mock()  # No exception raised

    # Patch requests.post to return mock response
    mock_post = mocker.patch("requests.post", return_value=mock_response)

    token = live_broker.authenticate()

    # Ensure requests.post was called with correct parameters
    mock_post.assert_called_once_with(
        f"{live_broker.BASE_URL}/sessions",
        json={"login": live_broker.username, "password": live_broker.password},
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    )

    # Ensure the token was properly extracted and stored
    assert token == "test_token"
    assert live_broker.token == "test_token"

def test_authenticate_failure_invalid_credentials(mocker, live_broker):
    """Test authentication failure when invalid credentials are provided."""
    mock_response = mocker.Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {"error": "Unauthorized"}
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized")

    # Patch requests.post to return mock response
    mock_post = mocker.patch("requests.post", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        live_broker.authenticate()

    # Ensure requests.post was called with correct parameters
    mock_post.assert_called_once()

def test_authenticate_failure_no_token(mocker, live_broker):
    """Test authentication failure when no session token is returned."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {}}  # No session-token
    mock_response.raise_for_status = mocker.Mock()

    # Patch requests.post to return mock response
    mock_post = mocker.patch("requests.post", return_value=mock_response)

    with pytest.raises(ValueError, match="❌ No token received in authentication response."):
        live_broker.authenticate()

    # Ensure requests.post was called with correct parameters
    mock_post.assert_called_once()

def test_place_order_dry_run(broker):
    """Test that place_order does not execute real trades in dry run mode."""
    order_details = {
        "symbol": "AAPL",
        "quantity": 1,
        "order_type": "limit",
        "price": 150.00,
    }

    result = broker.place_order(**order_details)

    # Ensure the function returns a simulated order
    assert result["status"] == "simulated"
    assert result["order"]["symbol"] == "AAPL"
    assert result["order"]["quantity"] == 1
    assert result["order"]["order_type"] == "limit"
    assert result["order"]["price"] == 150.00

def test_place_order_success(mocker, live_broker):
    """Test successful order placement in live mode."""
    order_details = {
        "symbol": "AAPL",
        "quantity": 1,
        "order_type": "limit",
        "price": 150.00,
    }

    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"status": "success", "order_id": "12345"}

    # Ensure raise_for_status() does nothing (successful request)
    mock_response.raise_for_status = mocker.Mock()

    # Patch 'requests.post' to return the mock response
    mock_post = mocker.patch("requests.post", return_value=mock_response)

    result = live_broker.place_order(**order_details)

    # Ensure requests.post() was called correctly
    mock_post.assert_called_once_with(
        f"{live_broker.BASE_URL}/orders",
        json=order_details,
        headers={"Authorization": "Bearer mock_token"},
    )

    # Ensure the function returns the expected API response
    assert result["status"] == "success"
    assert result["order_id"] == "12345"

def test_place_order_failure(mocker, live_broker):
    """Test that place_order raises an error when the API returns a failure."""
    order_details = {
        "symbol": "AAPL",
        "quantity": 1,
        "order_type": "limit",
        "price": 150.00,
    }

    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Invalid order"}

    # Simulate raise_for_status() raising an HTTP error
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("400 Client Error: Bad Request")

    # Patch 'requests.post' to return the mock response
    mock_post = mocker.patch("requests.post", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        live_broker.place_order(**order_details)

    # Ensure requests.post() was called
    mock_post.assert_called_once_with(
        f"{live_broker.BASE_URL}/orders",
        json=order_details,
        headers={"Authorization": "Bearer mock_token"},
    )

    # Ensure raise_for_status() was actually triggered
    mock_response.raise_for_status.assert_called_once()

def test_save_remember_me_token(live_broker, temp_remember_me_file):
    """Test that save_remember_me_token() correctly writes a token to a file."""
    live_broker.remember_me_file = str(temp_remember_me_file)  # Override file path
    test_token = "test123"

    live_broker.save_remember_me_token(test_token)

    # Verify the file was created
    assert os.path.exists(temp_remember_me_file)

    # Verify the saved token content
    with open(temp_remember_me_file, "r") as file:
        data = json.load(file)
        assert data["token"] == test_token

def test_load_remember_me_token_exists(live_broker, temp_remember_me_file):
    """Test that load_remember_me_token() correctly loads a token from a file."""
    live_broker.remember_me_file = str(temp_remember_me_file)  # Override file path
    test_token = "test123"

    # Create the file with token data
    with open(temp_remember_me_file, "w") as file:
        json.dump({"token": test_token}, file)

    # Verify the token is loaded correctly
    loaded_token = live_broker.load_remember_me_token()
    assert loaded_token == test_token

def test_load_remember_me_token_missing(live_broker, temp_remember_me_file):
    """Test that load_remember_me_token() returns None if the file does not exist."""
    live_broker.remember_me_file = str(temp_remember_me_file)  # Override file path

    # Ensure the file does not exist
    if os.path.exists(temp_remember_me_file):
        os.remove(temp_remember_me_file)

    # Verify the function returns None when file is missing
    assert live_broker.load_remember_me_token() is None
