from abc import ABC, abstractmethod
from typing import Optional
import json
from jedgebot.utils.logging import logger
from jedgebot.common.enums import OrderType  # ✅ Import from the new module


class Order(ABC):
    """Abstract base class for different types of orders."""

    def __init__(
        self,
        symbol: str,
        quantity: float,
        price: float,
        order_type: OrderType,
        expiration_date: Optional[str] = None,
    ):
        if not isinstance(order_type, OrderType):
            raise ValueError("Invalid order type. Use OrderType Enum.")

        self.symbol = symbol.upper()
        self.quantity = quantity
        self.price = price
        self.order_type = order_type  # ✅ Now using Enum from common location
        self.expiration_date = expiration_date


    @abstractmethod
    def execute(self):
        """Abstract method to execute an order."""
        pass

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(symbol={self.symbol}, quantity={self.quantity}, "
            f"price={self.price}, order_type={self.order_type.name}, expiration_date={self.expiration_date})"
        )

    def to_json(self):
        """
        Serialize the order to JSON format.
        """
        return json.dumps(
            {
                "symbol": self.symbol,
                "quantity": self.quantity,
                "price": self.price,
                "order_type": self.order_type.value,  # ✅ Using `.value` for JSON format
                "expiration_date": self.expiration_date,
            }
        )


class StockOrder(Order):
    """
    Concrete class for stock orders.
    """

    def __init__(self, symbol: str, quantity: int, price: float, order_type: OrderType):
        super().__init__(symbol, quantity, price, order_type)

    def execute(self):
        """
        Execute a stock order.
        """
        print(
            f"Executing {self.order_type.name} Stock Order: {self.quantity} shares of {self.symbol} at ${self.price}"
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
        order_type: OrderType,
        expiration_date: str,
        strike_price: float,
        option_type: str,
    ):
        """
        Initialize an Option Order.
        """
        super().__init__(symbol, quantity, price, order_type, expiration_date)
        self.strike_price = strike_price
        self.option_type = option_type

    def execute(self):
        """
        Execute an option order.
        """
        print(
            f"Executing {self.order_type.name} Option Order: {self.quantity} {self.option_type.upper()} contracts of {self.symbol} "
            f"at ${self.price}, Strike Price: ${self.strike_price}, Expiry: {self.expiration_date}"
        )


class CryptoOrder(Order):
    """
    Concrete class for cryptocurrency orders.
    """

    def __init__(
        self,
        symbol: str,
        quantity: float,
        price: float,
        order_type: OrderType,
        exchange: str,
    ):
        super().__init__(symbol, quantity, price, order_type)
        self.exchange = exchange

    def execute(self):
        """
        Execute a crypto order.
        """
        print(
            f"Executing {self.order_type.name} Crypto Order: {self.quantity} {self.symbol} at ${self.price} on {self.exchange}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(symbol={self.symbol}, quantity={self.quantity}, "
            f"price={self.price}, order_type={self.order_type.name}, exchange={self.exchange})"
        )
