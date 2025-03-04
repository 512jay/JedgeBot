import requests
from loguru import logger

class OrderService:
    """
    Handles order-related operations for the Tastytrade API.
    """

    def __init__(self, api_client):
        self.api_client = api_client
        self.base_url = "https://api.tastytrade.com"  # Ensure this is the correct base URL

    def place_order(self, account_number, order_payload):
        """
        Places an order on the Tastytrade platform.
        """
        url = f"{self.base_url}/accounts/{account_number}/orders"  # Ensure correct endpoint
        headers = self.api_client.get_headers()
        
        logger.info(f"Placing order for account {account_number} with payload: {order_payload}")
        
        response = requests.post(url, json=order_payload, headers=headers)
        
        if response.status_code == 201:
            logger.success("Order placed successfully.")
            return response.json()
        else:
            logger.error(f"Failed to place order: {response.status_code}, {response.text}")
            return None

    def get_orders(self, account_number):
        """
        Retrieves all orders for the given account.
        """
        url = f"{self.base_url}/accounts/{account_number}/orders"
        headers = self.api_client.get_headers()
        
        logger.info(f"Fetching orders for account {account_number}")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            logger.success("Orders fetched successfully.")
            return response.json()
        else:
            logger.error(f"Failed to fetch orders: {response.status_code}, {response.text}")
            return None

    def cancel_order(self, account_number, order_id):
        """
        Cancels an order for the given account.
        """
        url = f"{self.base_url}/accounts/{account_number}/orders/{order_id}"
        headers = self.api_client.get_headers()
        
        logger.info(f"Attempting to cancel order {order_id} for account {account_number}")
        
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 200:
            logger.success("Order canceled successfully.")
            return response.json()
        else:
            logger.error(f"Failed to cancel order: {response.status_code}, {response.text}")
            return None
