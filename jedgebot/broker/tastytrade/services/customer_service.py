from jedgebot.broker.tastytrade.api_client import APIClient


class CustomerService:
    """
    Service class for handling customer-related operations via the Tastytrade API.
    """
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get_customer_info(self):
        """Retrieve customer information."""
        endpoint = "/customers/me"
        response = self.api_client.get(endpoint)
        return response.get("data", {})

    def get_customer_accounts(self):
        """Retrieve accounts associated with the customer."""
        endpoint = "/customers/me/accounts"
        response = self.api_client.get(endpoint)
        return response.get("data", {}).get("items", [])
