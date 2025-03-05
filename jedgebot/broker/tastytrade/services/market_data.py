class MarketDataService:
    """
    Service class for handling market data retrieval from the Tastytrade API.
    """
    def __init__(self, api_client):
        """Initialize with shared API client."""
        self.api_client = api_client

    def get_market_data(self, symbol: str):
        """Fetches market data for a given stock symbol from Tastytrade."""
        endpoint = f"/market-data/{symbol}/quotes"
        response = self.api_client.get(endpoint)
        return response.get("data", {})

    def get_option_chain(self, symbol: str):
        """Fetches the option chain for a given stock symbol from Tastytrade."""
        endpoint = f"/market-data/{symbol}/options"
        response = self.api_client.get(endpoint)
        return response.get("data", {}).get("items", [])
