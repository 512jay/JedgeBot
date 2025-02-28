# jedgebot/broker/tastytrade_broker.py

import requests
import os
import json
from dotenv import load_dotenv
from jedgebot.broker.base_broker import BaseBroker

class TastyTradeBroker(BaseBroker):
    """Implementation of BaseBroker for TastyTrade API."""

    BASE_URL = "https://api.tastytrade.com"

    def __init__(self):
        load_dotenv()
        self.username = os.getenv("TASTYTRADE_USERNAME")
        self.password = os.getenv("TASTYTRADE_PASSWORD")
        self.remember_me_file = "remember_me_token.json"
        self.token = self.load_remember_me_token() or self.authenticate()
    
    def authenticate(self):
        """Authenticate with TastyTrade and retrieve a session token."""
        response = requests.post(
            f"{self.BASE_URL}/sessions",
            json={"login": self.username, "password": self.password}
        )
        response.raise_for_status()
        self.token = response.json().get("token")
        self.save_remember_me_token(self.token)
        return self.token

    def save_remember_me_token(self, token):
        """Saves the remember-me token to a file."""
        with open(self.remember_me_file, "w") as file:
            json.dump({"token": token}, file)
    
    def load_remember_me_token(self):
        """Loads the remember-me token from a file."""
        if os.path.exists(self.remember_me_file):
            with open(self.remember_me_file, "r") as file:
                data = json.load(file)
                return data.get("token")
        return None
    
    def get_account_balance(self):
        """Fetch account balance from TastyTrade."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.BASE_URL}/accounts", headers=headers)
        response.raise_for_status()
        return response.json()

    def place_order(self, symbol: str, quantity: int, order_type: str, price: float = None):
        """Place an order on TastyTrade."""
        headers = {"Authorization": f"Bearer {self.token}"}
        order_data = {
            "symbol": symbol,
            "quantity": quantity,
            "order_type": order_type,
        }
        if price:
            order_data["price"] = price  # Include price for limit orders

        response = requests.post(f"{self.BASE_URL}/orders", json=order_data, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_market_data(self, symbol: str):
        """Retrieve market data from TastyTrade."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.BASE_URL}/market-data/{symbol}", headers=headers)
        response.raise_for_status()
        return response.json()

    def get_order_status(self, order_id: str):
        """Retrieve the status of an order."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.BASE_URL}/orders/{order_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    def cancel_order(self, order_id: str):
        """Cancel an open order."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(f"{self.BASE_URL}/orders/{order_id}", headers=headers)
        response.raise_for_status()
        return {"status": "Order canceled"}

    def get_open_orders(self):
        """Retrieve all open orders."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.BASE_URL}/orders/open", headers=headers)
        response.raise_for_status()
        return response.json()

    def get_trade_history(self, start_date: str, end_date: str):
        """Fetch trade history."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(
            f"{self.BASE_URL}/trade-history?start={start_date}&end={end_date}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def get_buying_power(self):
        """Retrieve buying power."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.BASE_URL}/accounts/buying-power", headers=headers)
        response.raise_for_status()
        return response.json()

    def stream_market_data(self, symbols: list, callback):
        """Subscribe to real-time market data (Requires WebSocket setup)."""
        raise NotImplementedError("TastyTrade WebSocket streaming is not yet implemented.")
