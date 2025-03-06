import time
import requests
from log_setup import logger  # ✅ Now using centralized logging


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

    def _send_request(self, method, endpoint, **kwargs):
        """
        Sends an HTTP request to the Tastytrade API with one retry on 401 Unauthorized
        and exponential backoff on 429 Too Many Requests.

        :param method: HTTP method (GET, POST, PUT, DELETE).
        :param endpoint: API endpoint path.
        :param kwargs: Additional parameters for the request (params, json, etc.).
        :return: JSON response if successful, None if all retries fail.
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        retries = 0

        while retries < self.MAX_RETRIES:
            logger.info(f"🔍 {method} {url} - Attempt {retries + 1}")

            response = requests.request(method, url, headers=headers, **kwargs)
            result = self._handle_response(response, method, endpoint, kwargs, retries)

            if result is not None:
                return result

            retries += 1
            wait_time = 2 ** retries  # Exponential backoff: 2s → 4s → 8s
            logger.warning(f"⏳ Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

        logger.error("🚨 All retry attempts failed. Request aborted.")
        return None

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

    def post(self, endpoint, data=None):
        """
        Sends a POST request to a Tastytrade API endpoint.

        :param endpoint: API endpoint (e.g., "/accounts/{account_number}/orders").
        :param data: Optional dictionary of request payload.
        :return: JSON response or raises an error.
        """
        return self._send_request("POST", endpoint, json=data)

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
