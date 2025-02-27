import requests
import json
import time

class TastyTradeAPI:
    BASE_URL = "https://api.tastytrade.com"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session_token = None
        self.account_id = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with TastyTrade and get session token."""
        url = f"{self.BASE_URL}/sessions"
        payload = {"login": self.username, "password": self.password}
        response = requests.post(url, json=payload)
        
        if response.status_code == 201:
            data = response.json()
            self.session_token = data.get("data", {}).get("session-token")
            print("✅ Authentication successful!")
            self.get_account_id()
        else:
            raise Exception(f"❌ Authentication failed: {response.text}")

    def get_headers(self):
        """Returns authentication headers for API requests."""
        if not self.session_token:
            raise Exception("Not authenticated. Call authenticate() first.")
        return {"Authorization": f"Bearer {self.session_token}"}

    def get_account_id(self):
        """Fetches account ID for trading."""
        url = f"{self.BASE_URL}/customers/me/accounts"
        response = requests.get(url, headers=self.get_headers())
        
        if response.status_code == 200:
            accounts = response.json().get("data", [])
            if accounts:
                self.account_id = accounts[0]["account-number"]
                print(f"✅ Account ID: {self.account_id}")
            else:
                raise Exception("No accounts found!")
        else:
            raise Exception(f"Failed to fetch account ID: {response.text}")

    def get_balance(self):
        """Retrieves account balance and buying power."""
        url = f"{self.BASE_URL}/accounts/{self.account_id}/balances"
        response = requests.get(url, headers=self.get_headers())
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch balance: {response.text}")

    def place_order(self, symbol: str, quantity: int, action: str, order_type: str = "LIMIT", price: float = None):
        """Places an options order (buy/sell call/put)."""
        url = f"{self.BASE_URL}/accounts/{self.account_id}/orders"
        order_payload = {
            "symbol": symbol,
            "quantity": quantity,
            "action": action.upper(),
            "order-type": order_type.upper(),
            "price": price,
            "time-in-force": "GTC"  # Good Till Canceled
        }
        response = requests.post(url, json=order_payload, headers=self.get_headers())
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Order placement failed: {response.text}")

    def get_order_status(self, order_id: str):
        """Fetches the status of an order."""
        url = f"{self.BASE_URL}/accounts/{self.account_id}/orders/{order_id}"
        response = requests.get(url, headers=self.get_headers())
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch order status: {response.text}")

# Example Usage
if __name__ == "__main__":
    USERNAME = "your_username"
    PASSWORD = "your_password"
    
    tasty = TastyTradeAPI(USERNAME, PASSWORD)
    balance = tasty.get_balance()
    print(json.dumps(balance, indent=2))
    
    # Example order: Buy 1 SPY Call Option at $1.50
    order_response = tasty.place_order("SPY 20240228 500 C", 1, "BUY", "LIMIT", 1.50)
    print(json.dumps(order_response, indent=2))
