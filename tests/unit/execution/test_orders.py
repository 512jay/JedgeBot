import pytest
from backend.execution.order_manager import Order, StockOrder, CryptoOrder, OrderType


class MockOrder(Order):
    """
    A concrete subclass of Order for testing purposes.
    """

    def execute(self):
        return f"Executing order for {self.symbol}, quantity: {self.quantity}"


def test_order_cannot_be_instantiated():
    """
    Ensure that attempting to instantiate the abstract Order class raises an error.
    """
    with pytest.raises(TypeError):
        Order(symbol="AAPL", quantity=10, price=150.0, order_type=OrderType.LIMIT)


def test_mock_order_initialization():
    """
    Verify that a subclass of Order correctly initializes attributes.
    """
    mock_order = MockOrder(
        symbol="AAPL",
        quantity=10,
        price=150.0,
        order_type=OrderType.LIMIT,
        expiration_date="2025-12-31",
    )

    assert mock_order.symbol == "AAPL"
    assert mock_order.quantity == 10
    assert mock_order.price == 150.0
    assert mock_order.order_type == OrderType.LIMIT  # ✅ Correct usage
    assert mock_order.expiration_date == "2025-12-31"


def test_mock_order_execute():
    """
    Ensure that the execute method works correctly in the subclass.
    """
    mock_order = MockOrder(
        symbol="AAPL", quantity=10, price=150.0, order_type=OrderType.LIMIT
    )
    assert mock_order.execute() == "Executing order for AAPL, quantity: 10"


def test_order_repr():
    """
    Test the __repr__ method to ensure it returns the correct string representation.
    """
    mock_order = MockOrder(
        symbol="AAPL",
        quantity=10,
        price=150.0,
        order_type=OrderType.LIMIT,
        expiration_date="2025-12-31",
    )
    expected_repr = "MockOrder(symbol=AAPL, quantity=10, price=150.0, order_type=LIMIT, expiration_date=2025-12-31)"  # ✅ Updated
    assert repr(mock_order) == expected_repr


def test_stock_order_initialization():
    """
    Verify that StockOrder initializes correctly with valid attributes.
    """
    stock_order = StockOrder(
        symbol="AAPL", quantity=100, price=150.5, order_type=OrderType.LIMIT
    )

    assert stock_order.symbol == "AAPL"
    assert stock_order.quantity == 100
    assert stock_order.price == 150.5
    assert stock_order.order_type == OrderType.LIMIT
    assert (
        stock_order.expiration_date is None
    )  # ✅ Stock orders should not have an expiration date


def test_stock_order_inherits_from_order():
    """
    Ensure that StockOrder is a subclass of Order.
    """
    stock_order = StockOrder(
        symbol="AAPL", quantity=100, price=150.5, order_type=OrderType.LIMIT
    )
    assert isinstance(stock_order, Order)


def test_stock_order_execute(capsys):
    """
    Ensure that executing a StockOrder prints the expected output.
    """
    stock_order = StockOrder(
        symbol="AAPL", quantity=50, price=200.0, order_type=OrderType.MARKET
    )
    stock_order.execute()

    captured = capsys.readouterr()  # Capture printed output
    expected_output = "Executing MARKET Stock Order: 50 shares of AAPL at $200.0\n"
    assert captured.out == expected_output


def test_stock_order_repr():
    """
    Test the __repr__ method to ensure it returns the correct string representation.
    """
    stock_order = StockOrder(
        symbol="AAPL", quantity=100, price=150.5, order_type=OrderType.LIMIT
    )
    expected_repr = "StockOrder(symbol=AAPL, quantity=100, price=150.5, order_type=LIMIT, expiration_date=None)"  # ✅ Updated
    assert repr(stock_order) == expected_repr


class MockCryptoOrder(CryptoOrder):
    """
    A concrete subclass of CryptoOrder for testing purposes.
    """

    def execute(self):
        return f"Executing {self.order_type.name} Crypto Order: {self.quantity} {self.symbol} at ${self.price} on {self.exchange}"


def test_mock_crypto_order_initialization():
    """
    Verify that a subclass of CryptoOrder correctly initializes attributes.
    """
    crypto_order = MockCryptoOrder(
        symbol="ETH",
        quantity=1.25,
        price=3200.5,
        order_type=OrderType.LIMIT,
        exchange="Kraken",
    )

    assert crypto_order.symbol == "ETH"
    assert crypto_order.quantity == 1.25
    assert crypto_order.price == 3200.5
    assert crypto_order.order_type == OrderType.LIMIT  # ✅ Correct usage
    assert crypto_order.exchange == "Kraken"


def test_mock_crypto_order_execute():
    """
    Ensure that the execute method works correctly in the subclass.
    """
    crypto_order = MockCryptoOrder(
        symbol="BTC",
        quantity=0.75,
        price=48000.0,
        order_type=OrderType.MARKET,
        exchange="Coinbase",
    )
    assert (
        crypto_order.execute()
        == "Executing MARKET Crypto Order: 0.75 BTC at $48000.0 on Coinbase"
    )


def test_crypto_order_repr():
    """
    Test the __repr__ method to ensure it returns the correct string representation.
    """
    crypto_order = MockCryptoOrder(
        symbol="ETH",
        quantity=1.25,
        price=3200.5,
        order_type=OrderType.LIMIT,
        exchange="Kraken",
    )
    expected_repr = "MockCryptoOrder(symbol=ETH, quantity=1.25, price=3200.5, order_type=LIMIT, exchange=Kraken)"  # ✅ Updated
    assert repr(crypto_order) == expected_repr
