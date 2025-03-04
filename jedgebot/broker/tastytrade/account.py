class Account:
    def __init__(self, auth):
        """Initialize with an Authentication instance."""
        self.auth = auth  # Use Authentication instead of APIClient

    def get_accounts(self):
        """Fetch all accounts the authenticated user has access to."""
        endpoint = "accounts"
        return self.auth.make_request(endpoint)

    def get_account_details(self, account_id):
        """Fetch details for a specific account."""
        endpoint = f"accounts/{account_id}"
        return self.auth.make_request(endpoint)

    def get_account_balances(self, account_id):
        """Fetch balance details for a specific account."""
        endpoint = f"accounts/{account_id}/balances"
        return self.auth.make_request(endpoint)
