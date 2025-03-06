import os
from dotenv import load_dotenv
from jedgebot.broker.tastytrade.services.api_client import TastyTradeAPIClient
from jedgebot.broker.tastytrade.services.authentication import TastyTradeAuthenticator
from jedgebot.broker.tastytrade.services.customer import TastytradeCustomerService
from jedgebot.broker.tastytrade.services.order import OrderService
from jedgebot.broker.tastytrade.services.market_data import MarketDataService
from jedgebot.broker.tastytrade.services.account import TastyTradeAccount
from jedgebot.broker.tastytrade.services.account_stream import TastyTradeAccountStream
from jedgebot.broker.tastytrade.data_handler import TastyTradeDataHandler

# Load environment variables from .env
load_dotenv()

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
            raise ValueError("❌ Tastytrade username or password is missing. Set it in .env or provide manually.")

        self.auth = TastyTradeAuthenticator(self.username, self.password)
        self.api_client = TastyTradeAPIClient(self.auth)
        self.customer = TastytradeCustomerService(self.api_client)
        self.order = OrderService(self.api_client)
        self.market_data = MarketDataService(self.api_client)
        self.account = TastyTradeAccount(self.api_client)
        self.data_handler = TastyTradeDataHandler()
        self.account_stream = None  # Stream handler initialized lazily

    def refresh_authentication(self):
        """Refresh authentication tokens if needed."""
        self.auth.ensure_authenticated()

    def get_accounts(self):
        """Retrieve all accounts associated with the authenticated Tastytrade user."""
        return self.account.get_accounts()
    
    def get_account_number(self, index=0):
        """Retrieve the account number at the given index."""
        return self.account.get_account(index)

    def place_order(self, account_number: str, order_data: dict):
        """Place an order for a given Tastytrade account."""
        return self.order.place_order(account_number, order_data)

    def get_orders(self, account_number: str):
        """Retrieve all orders for a given Tastytrade account."""
        return self.order.get_orders(account_number)

    def get_market_data(self, symbol: str):
        """Fetch market data for a given symbol from Tastytrade."""
        return self.market_data.get_market_data(symbol)

    def get_customer_info(self):
        """Retrieve customer details for the authenticated user."""
        return self.customer.get_customer_info()

    def get_latest_data(self, data_type: str):
        """Retrieve the latest data from DataHandler."""
        return self.data_handler.get_data(data_type)

    def update_data(self, data_type: str, data: dict):
        """Update the data in DataHandler."""
        self.data_handler.update_data(data_type, data)

    def start_account_stream(self, account_number: str):
        """Start streaming account updates."""
        if self.account_stream is None:
            self.account_stream = TastyTradeAccountStream(self.auth, self.data_handler)
        self.account_stream.start_stream(account_number)

    def stop_account_stream(self):
        """Stop streaming account updates."""
        if self.account_stream:
            self.account_stream.stop_stream()

    def logout(self):
        """Logout and clear session tokens."""
        self.auth.logout()
        self.stop_account_stream()
