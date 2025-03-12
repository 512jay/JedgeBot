# execution/orders.py
from abc import ABC, abstractmethod
from typing import Optional

class Order(ABC):
    """
    Abstract base class for different types of orders (stock, options).
    """

    def __init__(
        self,
        symbol: str,
        quantity: float,
        price: float,
        order_type: str,
        expiration_date: Optional[str] = None,
    ):
        """
        Initialize the base Order class.

        :param symbol: The trading symbol (e.g., "AAPL", "SPY").
        :param quantity: The number of shares or contracts.
        :param price: The price at which to place the order.
        :param order_type: The type of order (e.g., "market", "limit", "stop").
        :param expiration_date: Expiration date for options (optional).
        """
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.expiration_date = expiration_date  # Only used for options

    @abstractmethod
    def execute(self):
        """
        Abstract method that must be implemented by subclasses to execute an order.
        """
        pass

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(symbol={self.symbol}, quantity={self.quantity}, "
            f"price={self.price}, order_type={self.order_type}, expiration_date={self.expiration_date})"
        )


class StockOrder(Order):
    """
    Concrete class for stock orders.
    """

    def __init__(self, symbol: str, quantity: int, price: float, order_type: str):
        super().__init__(symbol, quantity, price, order_type)

    def execute(self):
        """
        Execute a stock order.
        """
        print(
            f"Executing Stock Order: {self.quantity} shares of {self.symbol} at ${self.price} ({self.order_type})"
        )


class OptionOrder(Order):
    """
    Concrete class for option orders.
    """

    def __init__(
        self,
        symbol: str,
        quantity: int,
        price: float,
        order_type: str,
        expiration_date: str,
        strike_price: float,
        option_type: str,
    ):
        """
        Initialize an Option Order.

        :param strike_price: The strike price of the option.
        :param option_type: "call" or "put".
        """
        super().__init__(symbol, quantity, price, order_type, expiration_date)
        self.strike_price = strike_price
        self.option_type = option_type

    def execute(self):
        """
        Execute an option order.
        """
        print(
            f"Executing Option Order: {self.quantity} {self.option_type.upper()} contracts of {self.symbol} "
            f"at ${self.price} ({self.order_type}), Strike Price: ${self.strike_price}, Expiry: {self.expiration_date}"
        )


class CryptoOrder(Order):
    """
    Abstract base class for cryptocurrency orders.
    """

    def __init__(
        self, symbol: str, quantity: float, price: float, order_type: str, exchange: str
    ):
        """
        Initialize a Crypto Order.

        :param exchange: The exchange where the order will be executed (e.g., "Binance", "Kraken").
        """
        super().__init__(symbol, quantity, price, order_type)
        self.exchange = exchange  # Crypto-specific attribute

    @abstractmethod
    def execute(self):
        """Abstract method to execute a crypto order."""
        pass

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(symbol={self.symbol}, quantity={self.quantity}, "
            f"price={self.price}, order_type={self.order_type}, exchange={self.exchange})"
        )
