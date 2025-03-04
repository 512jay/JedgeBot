import requests
from loguru import logger
from jedgebot.broker.tastytrade.authentication import Authentication


class APIClient:
    """Handles HTTP requests to the Tastytrade API."""

    BASE_URL = "https://api.tastytrade.com"  # Update if necessary

    def __init__(self, authentication: Authentication):
        self.auth = authentication

    def _get_headers(self):
        """Returns the necessary headers including the authentication token."""
        token = self.auth.get_session_token()
        return {"Authorization": token, "Content-Type": "application/json"}

    def get(self, endpoint, params=None):
        """Sends a GET request to the given endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        logger.info(f"GET {url} - Params: {params}")
        response = requests.get(url, headers=headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data=None):
        """Sends a POST request to the given endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        logger.info(f"POST {url} - Data: {data}")
        response = requests.post(url, headers=headers, json=data)
        return self._handle_response(response)

    def put(self, endpoint, data=None):
        """Sends a PUT request to the given endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        logger.info(f"PUT {url} - Data: {data}")
        response = requests.put(url, headers=headers, json=data)
        return self._handle_response(response)

    def delete(self, endpoint):
        """Sends a DELETE request to the given endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        logger.info(f"DELETE {url}")
        response = requests.delete(url, headers=headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handles API responses, logging errors and returning data."""
        if response.status_code >= 400:
            logger.error(f"API Error {response.status_code}: {response.text}")
        response.raise_for_status()
        return response.json()
