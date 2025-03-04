from loguru import logger
import requests

class MarketDataService:
    """Handles market data retrieval from Tastytrade API."""

    def __init__(self, api_client):
        self.api_client = api_client
        logger.info("MarketDataService initialized")

    def get_market_data(self, symbol):
        """Fetches market data for a given symbol."""
        endpoint = f"/market-data/{symbol}"
        logger.info(f"Fetching market data for {symbol}")
        
        try:
            response = self.api_client.get(endpoint)
            response.raise_for_status()
            logger.info(f"Market data for {symbol} retrieved successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch market data for {symbol}: {e}")
            return None

    def get_quotes(self, symbol):
        """Fetches live quotes for a given symbol."""
        endpoint = f"/quotes/{symbol}"
        logger.info(f"Fetching live quotes for {symbol}")
        
        try:
            response = self.api_client.get(endpoint)
            response.raise_for_status()
            logger.info(f"Live quotes for {symbol} retrieved successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch live quotes for {symbol}: {e}")
            return None