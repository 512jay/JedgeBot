import time
import requests
from jedgebot.utils.logging import logger


class TastyTradeAPIClient:
    """Handles HTTP requests to the Tastytrade API."""

    BASE_URL = "https://api.tastytrade.com"
    RETRY_DELAY = 2  # Seconds before retrying after 401 Unauthorized
    MAX_RETRIES = 3  # Max retries for rate-limited requests (429)

    def __init__(self, auth):
        """
        Initialize API client with a shared authentication object.

        :param auth: Authentication object responsible for managing session tokens.
        """
        self.auth = auth  # ✅ Use shared auth object

    def _get_headers(self):
        """
        Fetches the latest authentication token and returns the required headers.

        :return: Dictionary containing the request headers.
        """
        token = self.auth.get_session_token()
        if not token:
            logger.error("🚨 No valid session token found! Re-authenticating...")
            token = self.auth.login()  # Force login if token is missing

        return {
            "Authorization": token,
            "Content-Type": "application/json",
        }

    def _handle_response(self, response, method, endpoint, kwargs, retry_count):
        """
        Handles API responses, logging errors and retrying once on 401 Unauthorized.
        Uses exponential backoff for 429 Too Many Requests.

        :param response: The response object from the HTTP request.
        :param method: HTTP method used in the request.
        :param endpoint: API endpoint requested.
        :param kwargs: Additional parameters passed in the request.
        :param retry_count: Current retry attempt number.
        :return: JSON response if successful, None if retry fails.
        """
        status_code = response.status_code

        if status_code == 401 and retry_count == 0:
            logger.warning("⚠️ Unauthorized! Re-authenticating in 2 seconds...")
            time.sleep(self.RETRY_DELAY)
            self.auth.login()
            return self._send_request(method, endpoint, **kwargs)

        if status_code == 401 and retry_count > 0:
            logger.error("🚨 Unauthorized again after retry! Aborting request.")
            return None

        if status_code == 429:
            logger.warning("⚠️ Rate limit exceeded. Applying exponential backoff...")
            return None

        if status_code >= 400:
            logger.error(f"🚨 API Error {status_code}: {response.text}")

        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params=None):
        """
        Sends a GET request to a Tastytrade API endpoint.

        :param endpoint: API endpoint (e.g., "/accounts/{account_number}/balances").
        :param params: Optional dictionary of query parameters.
        :return: JSON response or raises an error.
        """
        return self._send_request("GET", endpoint, params=params)

    def put(self, endpoint, data=None):
        """
        Sends a PUT request to a Tastytrade API endpoint.

        :param endpoint: API endpoint (e.g., "/accounts/{account_number}/settings").
        :param data: Optional dictionary of request payload.
        :return: JSON response or raises an error.
        """
        return self._send_request("PUT", endpoint, json=data)

    def delete(self, endpoint):
        """
        Sends a DELETE request to a Tastytrade API endpoint.

        :param endpoint: API endpoint (e.g., "/accounts/{account_number}/orders/{order_id}").
        :return: JSON response or raises an error.
        """
        return self._send_request("DELETE", endpoint)

    def post(self, endpoint, data=None):
        """
        Sends a POST request to a TastyTrade API endpoint.

        :param endpoint: API endpoint (e.g., "/accounts/{account_number}/orders").
        :param data: Optional dictionary of request payload.
        :return: JSON response or raises an error.
        """
        return self._send_request("POST", endpoint, json=data)

    def _send_request(self, method, endpoint, json=None, data=None, **kwargs):
        """
        Ensures both 'json' and 'data' parameters are explicitly handled.
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()

        logger.info(f"🔍 {method} {url} - Sending request with json={json} data={data}")

        response = requests.request(
            method, url, headers=headers, json=json, data=data, **kwargs
        )
        return self._handle_response(response, method, endpoint, kwargs, 0)
