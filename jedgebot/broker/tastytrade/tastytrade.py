from jedgebot.broker.tastytrade.api_client import TastyTradeAPIClient
from jedgebot.broker.tastytrade.authentication import TastyTradeAuthenticator
from jedgebot.broker.tastytrade.services.customer import TastytradeCustomerService
from jedgebot.broker.tastytrade.services.order import OrderService
from jedgebot.broker.tastytrade.services.market_data import MarketDataService
from jedgebot.broker.tastytrade.services.account import TastyTradeAccount

class TastytradeClient:
    def __init__(self, username: str, password: str):
        """Initialize the Tastytrade client with a shared authentication object."""
        self.auth = TastyTradeAuthenticator(username, password)  # ✅ Initialize once
        self.api_client = TastyTradeAPIClient(self.auth)  # ✅ Pass auth to API client
        self.customer = TastytradeCustomerService(self.api_client)  # ✅ Use shared auth
        self.order = OrderService(self.api_client)
        self.market_data = MarketDataService(self.api_client)
        self.account = TastyTradeAccount(self.api_client)  # ✅ Include account service

    def refresh_authentication(self):
        """Refresh authentication tokens if needed."""
        self.auth.ensure_authenticated()

    def get_accounts(self):
        """Retrieve all accounts associated with the authenticated Tastytrade user."""
        return self.account.get_accounts()
    
    def get_account_number(self, index=0):
        """Retrieve the account number at the given index."""
        return self.account.get_account(index)  # ✅ Delegate work to account.py

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

    def logout(self):
        """Logout and clear session tokens."""
        self.auth.logout()
