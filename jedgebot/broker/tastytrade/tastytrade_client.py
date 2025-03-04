from jedgebot.broker.tastytrade.api_client import APIClient
from jedgebot.broker.tastytrade.authentication import Authentication
from jedgebot.broker.tastytrade.services.account_service import AccountService
from jedgebot.broker.tastytrade.services.customer_service import CustomerService
from jedgebot.broker.tastytrade.services.order_service import OrderService
from jedgebot.broker.tastytrade.services.market_data_service import MarketDataService


class TastyTradeClient:
    def __init__(self, username: str, password: str):
        """Initialize the TastyTrade client with authentication."""
        self.auth = Authentication(username, password)
        self.api_client = APIClient(self.auth)
        self.account_service = AccountService(self.api_client)
        self.customer_service = CustomerService(self.api_client)
        self.order_service = OrderService(self.api_client)
        self.market_data_service = MarketDataService(self.api_client)

    def refresh_authentication(self):
        """Refresh authentication tokens."""
        self.auth.ensure_authenticated()

    def get_accounts(self):
        """Retrieve all accounts associated with the authenticated user."""
        return self.account_service.get_accounts()

    def place_order(self, account_number: str, order_data: dict):
        """Place an order for a given account."""
        return self.order_service.place_order(account_number, order_data)

    def get_orders(self, account_number: str):
        """Retrieve all orders for a given account."""
        return self.order_service.get_orders(account_number)

    def get_market_data(self, symbol: str):
        """Fetch market data for a given symbol."""
        return self.market_data_service.get_market_data(symbol)

    def get_customer_info(self):
        """Retrieve customer details for the authenticated user."""
        return self.customer_service.get_customer_info()

    def get_account_balances(self, account_number: str):
        """Retrieve account balances for a given account."""
        return self.account_service.get_account_balances(account_number)

    def logout(self):
        """Logout and clear session tokens."""
        self.auth.logout()
