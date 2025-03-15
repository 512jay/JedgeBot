import os
import asyncio
from typing import Optional
from backend.broker.tastytrade.services.market_data_streaming import (
    MarketDataStreamer,
)
from backend.broker.tastytrade.services.api_client import TastyTradeAPIClient
from backend.broker.tastytrade.services.authentication import (
    TastyTradeAuthenticator,
)
from backend.broker.tastytrade.services.customer import (
    TastytradeCustomerService,
)
from backend.broker.tastytrade.services.order import OrderService
from backend.broker.tastytrade.services.account import TastyTradeAccount
from backend.broker.tastytrade.services.account_streaming import (
    TastyTradeAccountStream,
)
from backend.broker.tastytrade.data_handler import TastyTradeDataHandler
from backend.broker.tastytrade.utilities import logout
from backend.utils.logging import logger


class TastyTradeClient:
    def __init__(self, username: str = None, password: str = None):
        """
        Initialize the Tastytrade client with a shared authentication object.

        :param username: Tastytrade username (optional, defaults to .env)
        :param password: Tastytrade password (optional, defaults to .env)
        """
        self.username = username or os.getenv("TASTYTRADE_USERNAME")
        self.password = password or os.getenv("TASTYTRADE_PASSWORD")

        if not self.username or not self.password:
            raise ValueError(
                "❌ Tastytrade username or password is missing. Set it in .env or provide manually."
            )

        self.auth = TastyTradeAuthenticator(self.username, self.password)
        self.api_client = TastyTradeAPIClient(self.auth)
        self.market_data_streamer = MarketDataStreamer(
            self
        )  # ✅ Pass the full client object
        self.customer = TastytradeCustomerService(self.api_client)
        self.order = OrderService(self.api_client)
        self.account = TastyTradeAccount(self.api_client)
        self.data_handler = TastyTradeDataHandler()
        self.account_stream = None  # Stream handler initialized lazily

    async def start_market_data_streaming(self, symbols: Optional[list[str]] = None):
        """Start automatic market data streaming."""
        await self.market_data_streamer.start_streaming(symbols)

    def start_account_stream(self):
        """Start streaming account updates."""
        if self.account_stream is None:
            self.account_stream = TastyTradeAccountStream(
                self
            )  # ✅ Pass self (TastyTradeClient)

        asyncio.create_task(
            self.account_stream.connect()
        )  # ✅ Start the async WebSocket

    def stop_account_stream(self):
        """Stop streaming account updates."""
        if self.account_stream:
            asyncio.create_task(self.account_stream.close())  # ✅ Use close()

    def logout(self, clear_session=False):
        """Logs out using the utility function while keeping the facade clean."""
        logout(self, clear_session)

    def refresh_authentication(self):
        """Refresh authentication tokens if needed."""
        logger.info("🔄 Refreshing authentication if needed...")
        self.auth.ensure_authenticated()

    def get_account_number(self, index=0):
        """Retrieve the account number at the given index."""
        logger.info(f"🔍 Fetching account number at index {index}...")
        return self.account.get_account(index)

    def update_data(self, data_type, data):
        """Update the data in DataHandler."""
        logger.info(f"🔄 Updating data for type: {data_type}...")
        self.data_handler.update_data(data_type, data)

    def get_accounts(self):
        """Retrieve all accounts associated with the authenticated Tastytrade user."""
        return self.account.get_accounts()

    def place_order(self, account_number: str, order_data: dict):
        """Place an order for a given Tastytrade account."""
        return self.order.place_order(account_number, order_data)

    def get_orders(self, account_number: str):
        """Retrieve all orders for a given Tastytrade account."""
        return self.order.get_orders(account_number)

    def get_customer_info(self):
        """Retrieve customer details for the authenticated user."""
        return self.customer.get_customer_info()

    def get_latest_data(self, data_type: str):
        """Retrieve the latest data from DataHandler."""
        return self.data_handler.get_data(data_type)
