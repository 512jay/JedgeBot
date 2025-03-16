from backend.utils.logging import logger


class TastytradeCustomerService:
    """Handles customer-related operations via the Tastytrade API."""

    def __init__(self, api_client):
        self.api_client = api_client  # ✅ Use shared API client

    def get_customer_info(self):
        """Retrieve customer information from Tastytrade."""
        endpoint = "/customers/me"
        response = self.api_client.get(endpoint)
        return response.get("data", {})

    def get_customer_accounts(self):
        """Retrieve accounts associated with the customer."""
        endpoint = "/customers/me/accounts"
        response = self.api_client.get(endpoint)
        return response.get("data", {}).get("items", [])
