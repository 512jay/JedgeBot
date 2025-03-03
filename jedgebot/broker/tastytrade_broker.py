# jedgebot/broker/tastytrade_broker.py

import requests
import os
import json
from typing import Optional
from dotenv import load_dotenv
from loguru import logger
from jedgebot.broker.base_broker import BaseBroker
from jedgebot.api.request_utils import request_with_retry
from jedgebot.utils.logging_utils import setup_logger
# Explicitly point to the .env file inside jedgebot/
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "jedgebot", ".env")
load_dotenv(dotenv_path)

class TastyTradeBroker(BaseBroker):
    """Implementation of BaseBroker for TastyTrade API."""

    def __init__(self):
        # ✅ Explicitly reload .env every time a broker instance is created
        dotenv_path = os.path.join(os.path.dirname(__file__), "..", "jedgebot", ".env")
        load_dotenv(dotenv_path, override=True)

        self.ENV = os.getenv("TASTYTRADE_ENV", "live").lower()
        self.BASE_URL = "https://api.tastytrade.com" if self.ENV == "live" else "https://api.cert.tastytrade.com"
        
        # ✅ Read DRY_RUN at runtime to respect test overrides
        self.DRY_RUN = os.getenv("TASTYTRADE_DRY_RUN", "true").lower() == "true"

        if self.ENV == "paper":
            self.username = os.getenv("TASTYTRADE_PAPER_USERNAME")
            self.password = os.getenv("TASTYTRADE_PAPER_PASSWORD")
        else:
            self.username = os.getenv("TASTYTRADE_USERNAME")
            self.password = os.getenv("TASTYTRADE_PASSWORD")

        self.remember_me_file = "remember_me_token.json"
        self.logger = setup_logger("tastytrade")

        self.token = self.load_remember_me_token() or self.authenticate()

        if self.DRY_RUN:
            self.logger.info("🔄 Dry run mode enabled: No real trades will be executed.")
        else:
            self.logger.warning("⚠️ LIVE MODE: Real trades will be executed!")

    def authenticate(self):
        """Authenticate with TastyTrade and retrieve a session token."""
        try:
            url = f"{self.BASE_URL}/sessions"
            data = {"login": self.username, "password": self.password}  # Send correct password
            headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

            self.logger.info("🔐 Attempting authentication...")
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Ensure HTTP errors raise exceptions

            # Extract token correctly
            response_data = response.json()
            self.token = response_data.get("data", {}).get("session-token")

            if not self.token:
                raise ValueError("❌ No token received in authentication response.")

            self.save_remember_me_token(self.token)
            self.logger.info("✅ Authentication successful!")
            return self.token

        except requests.RequestException as e:
            self.logger.error(f"❌ Authentication failed: {e}")
            raise

    def get_account_balance(self):
        """Fetch account balance from TastyTrade."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(f"{self.BASE_URL}/accounts", headers=headers)
            response.raise_for_status()
            logger.info("✅ Account balance retrieved successfully")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"❌ Failed to fetch account balance: {e}")
            raise
    
    def place_order(self, symbol: str, quantity: int, order_type: str, price: Optional[float] = None):
        """Place an order on TastyTrade, supporting dry run mode."""
        headers = {"Authorization": f"Bearer {self.token}"}
        order_data = {
            "symbol": symbol,
            "quantity": quantity,
            "order_type": order_type,
        }
        if price:
            order_data["price"] = price  # Include price for limit orders
        
        if self.DRY_RUN:
            self.logger.info(f"📝 Dry run: Order NOT executed: {order_data}")
            return {"status": "simulated", "order": order_data}
        
        try:
            response = requests.post(f"{self.BASE_URL}/orders", json=order_data, headers=headers)
            response.raise_for_status()
            self.logger.info(f"✅ Order placed: {symbol}, Quantity: {quantity}, Type: {order_type}, Price: {price}")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"❌ Order placement failed: {e}")
            raise

    def cancel_order(self, order_id: str):
        """Cancel an open order."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.delete(f"{self.BASE_URL}/orders/{order_id}", headers=headers)
            response.raise_for_status()
            logger.info(f"✅ Order {order_id} canceled successfully")
            return {"status": "Order canceled"}
        except requests.RequestException as e:
            logger.error(f"❌ Failed to cancel order {order_id}: {e}")
            raise

    def get_market_data(self, symbol: str):
        """Retrieve market data from TastyTrade."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(f"{self.BASE_URL}/market-data/{symbol}", headers=headers)
            response.raise_for_status()
            logger.info(f"✅ Market data retrieved for {symbol}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"❌ Failed to retrieve market data for {symbol}: {e}")
            raise

    def get_trade_history(self, start_date: str, end_date: Optional[str] = None):
        """Fetch trade history."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(
                f"{self.BASE_URL}/trade-history?start={start_date}&end={end_date}",
                headers=headers,
            )
            response.raise_for_status()
            logger.info(f"✅ Trade history retrieved from {start_date} to {end_date}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"❌ Failed to retrieve trade history: {e}")
            raise

    def get_buying_power(self):
        """Retrieve buying power."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(f"{self.BASE_URL}/accounts/buying-power", headers=headers)
            response.raise_for_status()
            logger.info("✅ Buying power retrieved successfully")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"❌ Failed to retrieve buying power: {e}")
            raise

    def get_open_orders(self):
        """Retrieve all open orders (not yet implemented for TastyTrade)."""
        logger.warning("get_open_orders() is not implemented yet.")
        raise NotImplementedError("get_open_orders() is not implemented yet.")

    def get_order_status(self, order_id: str):
        """Retrieve the status of an order (not yet implemented for TastyTrade)."""
        logger.warning(f"get_order_status({order_id}) is not implemented yet.")
        raise NotImplementedError("get_order_status() is not implemented yet.")

    def stream_market_data(self, symbols: list, callback):
        """Subscribe to real-time market data (not yet implemented for TastyTrade)."""
        logger.warning(f"stream_market_data({symbols}) is not implemented yet.")
        raise NotImplementedError("stream_market_data() is not implemented yet.")
    
    def load_remember_me_token(self):
        """Loads the remember-me token from a file if it exists."""
        if os.path.exists(self.remember_me_file):
            with open(self.remember_me_file, "r") as file:
                data = json.load(file)
                return data.get("token")
        return None

    def save_remember_me_token(self, token):
        """Saves the remember-me token to a file."""
        with open(self.remember_me_file, "w") as file:
            json.dump({"token": token}, file)
