import tastytrade as tt
import os
from dotenv import load_dotenv

class TastyTradeAPI:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("TASTYTRADE_USERNAME")
        self.password = os.getenv("TASTYTRADE_PASSWORD")
        self.session = None
        self.account_id = None
        self.authenticate()

    def authenticate(self):
        """Authenticate using TastyTrade SDK."""
        try:
            tt.login(self.username, self.password)
            print("✅ Authentication successful!")
            self.get_account_id()
        except Exception as e:
            raise Exception(f"❌ Authentication failed: {e}")

    def get_account_id(self):
        """Fetches account ID for trading."""
        accounts = tt.Account.get_accounts()
        if accounts:
            self.account_id = accounts[0].account_number
            print(f"✅ Account ID: {self.account_id}")
        else:
            raise Exception("No accounts found!")

    def get_balance(self):
        """Retrieves account balance and buying power."""
        account = tt.Account.get_by_account_number(self.account_id)
        return account.get_balances()

    def place_order(self, symbol: str, quantity: int, action: str, order_type: str = "LIMIT", price: float = None):
        """Places an options order using TastyTrade SDK."""
        order = tt.Order(
            account=self.account_id,
            symbol=symbol,
            quantity=quantity,
            action=action.upper(),
            order_type=order_type.upper(),
            price=price,
            time_in_force="GTC"
        )
        response = order.place()
        return response

    def get_order_status(self, order_id: str):
        """Fetches the status of an order."""
        return tt.Order.get_by_order_id(order_id)

# Example Usage
if __name__ == "__main__":
    tasty = TastyTradeAPI()
    balance = tasty.get_balance()
    print(balance)
    
    # Example order: Buy 1 SPY Call Option at $1.50
    order_response = tasty.place_order("SPY 20240228 500 C", 1, "BUY", "LIMIT", 1.50)
    print(order_response)