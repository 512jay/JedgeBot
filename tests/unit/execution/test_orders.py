import pytest
from jedgebot.execution.orders import Order, StockOrder, CryptoOrder


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
        Order(symbol="AAPL", quantity=10, price=150.0, order_type="limit")


def test_mock_order_initialization():
    """
    Verify that a subclass of Order correctly initializes attributes.
    """
    mock_order = MockOrder(
        symbol="AAPL",
        quantity=10,
        price=150.0,
        order_type="limit",
        expiration_date="2025-12-31",
    )

    assert mock_order.symbol == "AAPL"
    assert mock_order.quantity == 10
    assert mock_order.price == 150.0
    assert mock_order.order_type == "limit"
    assert mock_order.expiration_date == "2025-12-31"


def test_mock_order_execute():
    """
    Ensure that the execute method works correctly in the subclass.
    """
    mock_order = MockOrder(symbol="AAPL", quantity=10, price=150.0, order_type="limit")
    assert mock_order.execute() == "Executing order for AAPL, quantity: 10"


def test_order_repr():
    """
    Test the __repr__ method to ensure it returns the correct string representation.
    """
    mock_order = MockOrder(
        symbol="AAPL",
        quantity=10,
        price=150.0,
        order_type="limit",
        expiration_date="2025-12-31",
    )
    expected_repr = "MockOrder(symbol=AAPL, quantity=10, price=150.0, order_type=limit, expiration_date=2025-12-31)"
    assert repr(mock_order) == expected_repr


def test_stock_order_initialization():
    """
    Verify that StockOrder initializes correctly with valid attributes.
    """
    stock_order = StockOrder(
        symbol="AAPL", quantity=100, price=150.5, order_type="limit"
    )

    assert stock_order.symbol == "AAPL"
    assert stock_order.quantity == 100
    assert stock_order.price == 150.5
    assert stock_order.order_type == "limit"
    assert (
        stock_order.expiration_date is None
    )  # Stock orders should not have an expiration date


def test_stock_order_inherits_from_order():
    """
    Ensure that StockOrder is a subclass of Order.
    """
    stock_order = StockOrder(
        symbol="AAPL", quantity=100, price=150.5, order_type="limit"
    )
    assert isinstance(stock_order, Order)


def test_stock_order_execute(capsys):
    """
    Ensure that executing a StockOrder prints the expected output.
    """
    stock_order = StockOrder(
        symbol="AAPL", quantity=50, price=200.0, order_type="market"
    )
    stock_order.execute()

    captured = capsys.readouterr()  # Capture printed output
    expected_output = "Executing Stock Order: 50 shares of AAPL at $200.0 (market)\n"
    assert captured.out == expected_output


def test_stock_order_repr():
    """
    Test the __repr__ method to ensure it returns the correct string representation.
    """
    stock_order = StockOrder(
        symbol="AAPL", quantity=100, price=150.5, order_type="limit"
    )
    expected_repr = "StockOrder(symbol=AAPL, quantity=100, price=150.5, order_type=limit, expiration_date=None)"
    assert repr(stock_order) == expected_repr


class MockCryptoOrder(CryptoOrder):
    """
    A concrete subclass of CryptoOrder for testing purposes.
    """

    def execute(self):
        return f"Executing Crypto Order: {self.quantity} {self.symbol} at ${self.price} ({self.order_type}) on {self.exchange}"


def test_crypto_order_cannot_be_instantiated():
    """
    Ensure that attempting to instantiate the abstract CryptoOrder class raises an error.
    """
    with pytest.raises(TypeError):
        CryptoOrder(
            symbol="BTC",
            quantity=0.5,
            price=45000.0,
            order_type="market",
            exchange="Binance",
        )


def test_mock_crypto_order_initialization():
    """
    Verify that a subclass of CryptoOrder correctly initializes attributes.
    """
    crypto_order = MockCryptoOrder(
        symbol="ETH", quantity=1.25, price=3200.5, order_type="limit", exchange="Kraken"
    )

    assert crypto_order.symbol == "ETH"
    assert crypto_order.quantity == 1.25
    assert crypto_order.price == 3200.5
    assert crypto_order.order_type == "limit"
    assert crypto_order.exchange == "Kraken"


def test_mock_crypto_order_execute():
    """
    Ensure that the execute method works correctly in the subclass.
    """
    crypto_order = MockCryptoOrder(
        symbol="BTC",
        quantity=0.75,
        price=48000.0,
        order_type="market",
        exchange="Coinbase",
    )
    assert (
        crypto_order.execute()
        == "Executing Crypto Order: 0.75 BTC at $48000.0 (market) on Coinbase"
    )


def test_crypto_order_repr():
    """
    Test the __repr__ method to ensure it returns the correct string representation.
    """
    crypto_order = MockCryptoOrder(
        symbol="ETH", quantity=1.25, price=3200.5, order_type="limit", exchange="Kraken"
    )
    expected_repr = "MockCryptoOrder(symbol=ETH, quantity=1.25, price=3200.5, order_type=limit, exchange=Kraken)"
    assert repr(crypto_order) == expected_repr
