from abc import ABC, abstractmethod
from typing import Optional
from jedgebot.utils.logging import logger
from jedgebot.common.enums import OrderType


class BaseBroker(ABC):
    """Abstract base class for broker integrations."""

    @abstractmethod
    def authenticate(self):
        """Authenticate with the broker's API."""
        pass

    @abstractmethod
    def get_account_balance(self):
        """Fetch the account balance."""
        pass

    @abstractmethod
    def place_order(
        self,
        symbol: str,
        quantity: int,
        order_type: OrderType,  # ✅ Now using Enum from common location
        price: Optional[float] = None,
    ):
        """
        Place an order.

        :param symbol: The asset to trade (e.g., "AAPL")
        :param quantity: Number of shares/contracts
        :param order_type: OrderType Enum ("MARKET", "LIMIT", etc.)
        :param price: Required for limit orders
        """
        pass

    @abstractmethod
    def get_market_data(self, symbol: str):
        """Retrieve market data for a symbol."""
        pass

    @abstractmethod
    def get_order_status(self, order_id: str):
        """Retrieve the status of an existing order."""
        pass

    @abstractmethod
    def cancel_order(self, order_id: str):
        """Cancel an open order."""
        pass

    @abstractmethod
    def get_open_orders(self):
        """Retrieve all open orders."""
        pass

    @abstractmethod
    def get_trade_history(self, start_date: str, end_date: str):
        """Fetch trade history for a given date range."""
        pass

    @abstractmethod
    def get_buying_power(self):
        """Retrieve available buying power or margin information."""
        pass

    @abstractmethod
    def stream_market_data(self, symbols: list, callback):
        """Subscribe to real-time market data."""
        pass
