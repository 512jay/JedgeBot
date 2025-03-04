import logging
from jedgebot.broker.tastytrade.api_client import APIClient


class AccountService:
    """Service for managing account-related operations."""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get_accounts(self):
        """Fetch accounts from the API."""
        response = self.api_client.get("/customers/me/accounts")
        if response and "data" in response and "items" in response["data"]:
            return [item["account"]["account-number"] for item in response["data"]["items"]]
        return []

    def get_account_details(self, account_number: str):
        """Retrieve detailed information about a specific account."""
        endpoint = f"/accounts/{account_number}"
        response = self.api_client.get(endpoint)
        return response.get("data", {})

    def get_account_balances(self, account_number: str):
        """Retrieve balance details for a specific account."""
        endpoint = f"/accounts/{account_number}/balances"
        response = self.api_client.get(endpoint)
        return response.get("data", {})

    def get_account_positions(self, account_number: str):
        """Retrieve positions for a specific account."""
        endpoint = f"/accounts/{account_number}/positions"
        response = self.api_client.get(endpoint)
        return response.get("data", [])

    def get_account_orders(self, account_number: str):
        """Retrieve all orders for a specific account."""
        endpoint = f"/accounts/{account_number}/orders"
        response = self.api_client.get(endpoint)
        return response.get("data", [])
