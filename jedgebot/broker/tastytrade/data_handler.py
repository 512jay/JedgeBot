class TastyTradeDataHandler:
    """Manages account data updates received via WebSocket."""
    
    def __init__(self):
        self.account_data = {}

    def update_account_data(self, data):
        """Store the latest account update from WebSocket stream."""
        account_id = data.get("account-number")
        if account_id:
            self.account_data[account_id] = data
            print(f"✅ Data Updated for Account {account_id}")

    def get_account_data(self, account_id):
        """Retrieve the latest stored account data."""
        return self.account_data.get(account_id, {})
