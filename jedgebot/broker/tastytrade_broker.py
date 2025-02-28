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


class TastyTradeBroker(BaseBroker):
    """Implementation of BaseBroker for TastyTrade API."""

    BASE_URL = "https://api.tastytrade.com"

    def __init__(self):
        load_dotenv()
        self.username = os.getenv("TASTYTRADE_USERNAME")
        self.password = os.getenv("TASTYTRADE_PASSWORD")
        self.remember_me_file = "remember_me_token.json"
        self.token = self.load_remember_me_token() or self.authenticate()

        # Setup logger
        logger.add("logs/tastytrade.log", rotation="1 MB", retention="7 days", level="INFO")
        logger.info("TastyTradeBroker initialized")

    def authenticate(self):
        """Authenticate with TastyTrade and retrieve a session token."""
        try:
            url = f"{self.BASE_URL}/sessions"
            data = {"login": self.username, "password": "[REDACTED]"}  # Mask password in logs
            response = request_with_retry(url, method="POST", data=data)
            self.token = response.get("token")
            self.save_remember_me_token(self.token)
            logger.info("✅ Authentication successful!")
            return self.token
        except requests.RequestException as e:
            logger.error(f"❌ Authentication failed: {e}")
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
        """Place an order on TastyTrade."""
        headers = {"Authorization": f"Bearer {self.token}"}
        order_data = {
            "symbol": symbol,
            "quantity": quantity,
            "order_type": order_type,
        }
        if price:
            order_data["price"] = price  # Include price for limit orders

        try:
            response = requests.post(f"{self.BASE_URL}/orders", json=order_data, headers=headers)
            response.raise_for_status()
            logger.info(f"✅ Order placed: {symbol}, Quantity: {quantity}, Type: {order_type}, Price: {price}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"❌ Order placement failed: {e}")
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
