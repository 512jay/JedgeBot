class Orders:
    def __init__(self, auth):
        """Initialize with an Authentication instance."""
        self.auth = auth  # Use Authentication instead of APIClient

    def place_order(self, account_id, symbol, quantity, order_type="LIMIT", price=None):
        """Place an order on TastyTrade."""
        endpoint = f"accounts/{account_id}/orders"
        payload = {
            "symbol": symbol,
            "quantity": quantity,
            "order-type": order_type,
            "price": price,
        }
        return self.auth.make_request(endpoint, method="POST", payload=payload)

    def get_orders(self, account_id):
        """Fetch all orders for a specific account."""
        endpoint = f"accounts/{account_id}/orders"
        return self.auth.make_request(endpoint)
