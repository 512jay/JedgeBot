import requests
from loguru import logger

class TastyTradeAPIClient:
    """Handles HTTP requests to the Tastytrade API."""

    BASE_URL = "https://api.tastytrade.com"

    def __init__(self, auth):
        """Initialize API client with a shared authentication object."""
        self.auth = auth  # ✅ Use shared auth object

    def _get_headers(self):
        """Fetches the latest authentication token and returns the required headers."""
        token = self.auth.get_session_token()
        if not token:
            logger.error("🚨 No valid session token found! Re-authenticating...")
            token = self.auth.login()  # Force login if token is missing

        return {"Authorization": token, "Content-Type": "application/json"}

    def get(self, endpoint, params=None):
        """Sends a GET request to a Tastytrade API endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        logger.info(f"🔍 GET {url} - Params: {params}")
        response = requests.get(url, headers=headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data=None):
        """Sends a POST request to a Tastytrade API endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        logger.info(f"📤 POST {url} - Data: {data}")
        response = requests.post(url, headers=headers, json=data)
        return self._handle_response(response)

    def put(self, endpoint, data=None):
        """Sends a PUT request to a Tastytrade API endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        logger.info(f"✏️ PUT {url} - Data: {data}")
        response = requests.put(url, headers=headers, json=data)
        return self._handle_response(response)

    def delete(self, endpoint):
        """Sends a DELETE request to a Tastytrade API endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        logger.info(f"🗑️ DELETE {url}")
        response = requests.delete(url, headers=headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handles API responses, logging errors and returning the parsed JSON response."""
        if response.status_code >= 400:
            logger.error(f"🚨 API Error {response.status_code}: {response.text}")

        response.raise_for_status()
        return response.json()
