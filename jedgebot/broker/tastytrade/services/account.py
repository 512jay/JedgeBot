import logging

class TastyTradeAccount:
    """Service for managing account-related operations."""

    def __init__(self, api_client):
        """Initialize with shared API client."""
        self.api_client = api_client

    def get_accounts(self):
        """Fetch accounts from the API."""
        response = self.api_client.get("/customers/me/accounts")

        # Debug: Print response to confirm structure
        # print("🔍 API Response:", response)

        # Ensure response structure is correct
        if isinstance(response, dict) and "data" in response and "items" in response["data"]:
            return response["data"]["items"]  # ✅ Return list of account objects

        return []  # ✅ Return an empty list if response format is unexpected

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

    def parse_accounts(self, response_json):
        """
        Extracts a list of account numbers from the TastyTrade API response.

        :param response_json: JSON response from the API.
        :return: List of account numbers.
        """
        try:
            return [acc["account"]["account-number"] for acc in response_json]
        except (KeyError, TypeError) as e:
            print(f"Error parsing accounts: {e}")
            return []

    def get_account(self, account_order_number: int = 0):
        """
        Returns the account number at the specified index.

        :param account_order_number: Index of the account in the list.
        :return: Account number as a string or None if not found.
        """
        accounts_json = self.get_accounts()
        account_numbers = self.parse_accounts(accounts_json)

        if 0 <= account_order_number < len(account_numbers):
            return account_numbers[account_order_number]  # ✅ Only return account number
        return None
