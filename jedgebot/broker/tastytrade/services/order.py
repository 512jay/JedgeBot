class OrderService:
    """
    Service class for handling order-related operations via the Tastytrade API.
    """
    def __init__(self, api_client):
        """Initialize with shared API client."""
        self.api_client = api_client

    def place_order(self, account_number: str, order_data: dict):
        """Places an order for a given Tastytrade account."""
        endpoint = f"/accounts/{account_number}/orders"
        response = self.api_client.post(endpoint, order_data)
        return response.get("data", {})

    def get_orders(self, account_number: str):
        """Retrieves all orders for a given Tastytrade account."""
        endpoint = f"/accounts/{account_number}/orders"
        response = self.api_client.get(endpoint)
        return response.get("data", {}).get("items", [])

    def cancel_order(self, account_number: str, order_id: str):
        """Cancels an existing order for a given Tastytrade account."""
        endpoint = f"/accounts/{account_number}/orders/{order_id}"
        response = self.api_client.delete(endpoint)
        return response.get("data", {})
