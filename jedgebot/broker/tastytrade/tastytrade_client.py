from .account import Account
from .authentication import Authentication
from .customer import Customer
from .orders import Orders


class TastyTradeClient:
    def __init__(self, username, password):
        self.auth = Authentication(username, password)
        self.orders = Orders(self.auth)
        self.account = Account(self.auth)
        self.customer = Customer(self.auth)

    def place_order(self, account_id, symbol, quantity, order_type="LIMIT", price=None):
        """Wrapper for placing an order."""
        return self.orders.place_order(account_id, symbol, quantity, order_type, price)

    def get_orders(self, account_id):
        """Wrapper for retrieving orders."""
        return self.orders.get_orders(account_id)

    def get_accounts(self):
        """Fetch all accounts the user has access to."""
        return self.account.get_accounts()

    def get_account_details(self, account_id):
        """Fetch details for a specific account."""
        return self.account.get_account_details(account_id)

    def get_account_balances(self, account_id):
        """Fetch balance details for a specific account."""
        return self.account.get_account_balances(account_id)

    def get_customer_info(self):
        """Fetch basic customer information."""
        return self.customer.get_customer_info()
    
    def save_customer_data(self, filename="customer_data.json"):
        """Fetch customer data and save it as a JSON file in the script directory."""
        return self.customer.save_customer_data(filename)  

    def get_customer_accounts(self):
        """Fetch customer account list."""
        return self.customer.get_customer_accounts()
    
    def save_customer_accounts(self, filename="customer_accounts.json"):
        """Fetch customer accounts and save them as a JSON file in the script directory."""
        return self.customer.save_customer_accounts(filename)
    
    def extract_account_numbers(self):
        """Extracts and returns a list of account numbers."""
        return self.customer.extract_account_numbers()
    
    def logout(self):
        """Logout the user."""
        return self.auth.logout()
    
