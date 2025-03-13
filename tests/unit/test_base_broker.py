import pytest
from typing import Optional
from jedgebot.broker.broker_api import BaseBroker


class MockBroker(BaseBroker):
    "Mock implementation of BaseBroker for testing purposes."

    def authenticate(self):
        return "Authenticated"

    def get_account_balance(self):
        return 10000.00

    def place_order(
        self,
        symbol: str,
        quantity: int,
        order_type: str,
        price: Optional[float] = None,
    ):
        return {
            "symbol": symbol,
            "quantity": quantity,
            "order_type": order_type,
            "price": price,
        }

    def get_market_data(self, symbol: str):
        return {"symbol": symbol, "price": 150.00}

    def get_order_status(self, order_id: str):
        return {"order_id": order_id, "status": "Filled"}

    def cancel_order(self, order_id: str):
        return f"Order {order_id} canceled"

    def get_open_orders(self):
        return []

    def get_trade_history(self, start_date: str, end_date: str):
        return [
            {
                "date": start_date,
                "symbol": "AAPL",
                "quantity": 10,
                "price": 150.00,
            }
        ]

    def get_buying_power(self):
        return 5000.00

    def stream_market_data(self, symbols, callback):
        for symbol in symbols:
            callback({"symbol": symbol, "price": 150.00})


# Tests
def test_cannot_instantiate_base_broker():
    """Ensure that BaseBroker cannot be instantiated directly."""
    with pytest.raises(
        TypeError,
        match="Can't instantiate abstract class BaseBroker with abstract methods",
    ):
        BaseBroker()


def test_can_instantiate_mock_broker():
    """Ensure that a fully implemented subclass of BaseBroker can be instantiated."""
    broker = MockBroker()
    assert isinstance(broker, BaseBroker)


def test_authenticate():
    broker = MockBroker()
    assert broker.authenticate() == "Authenticated"


def test_get_account_balance():
    broker = MockBroker()
    assert broker.get_account_balance() == 10000.00


def test_place_order():
    broker = MockBroker()
    order = broker.place_order("AAPL", 10, "market")
    assert order["symbol"] == "AAPL"
    assert order["quantity"] == 10
    assert order["order_type"] == "market"


def test_get_market_data():
    broker = MockBroker()
    data = broker.get_market_data("AAPL")
    assert data["symbol"] == "AAPL"
    assert data["price"] == 150.0


def test_get_order_status():
    broker = MockBroker()
    status = broker.get_order_status("12345")
    assert status["order_id"] == "12345"
    assert status["status"] == "Filled"


def test_cancel_order():
    broker = MockBroker()
    message = broker.cancel_order("12345")
    assert message == "Order 12345 canceled"


def test_get_open_orders():
    broker = MockBroker()
    assert broker.get_open_orders() == []


def test_get_trade_history():
    broker = MockBroker()
    history = broker.get_trade_history("2025-03-01", "2025-03-05")
    assert len(history) == 1
    assert history[0]["symbol"] == "AAPL"


def test_get_buying_power():
    broker = MockBroker()
    assert broker.get_buying_power() == 5000.0


def test_stream_market_data():
    broker = MockBroker()
    results = []

    def mock_callback(data):
        results.append(data)

    broker.stream_market_data(["AAPL", "TSLA"], mock_callback)
    assert len(results) == 2
    assert results[0]["symbol"] == "AAPL"
    assert results[1]["symbol"] == "TSLA"
