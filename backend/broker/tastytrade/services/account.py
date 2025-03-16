import time
from backend.utils.logging import logger


class TastyTradeAccount:
    """Handles account-related operations for Tastytrade."""

    CACHE_EXPIRY = 60  # Cache expires after 60 seconds

    def __init__(self, api_client):
        """
        Initializes the account service with a shared API client.

        :param api_client: Instance of TastyTradeAPIClient to make API requests.
        """
        self.api_client = api_client
        self._balances = None  # ✅ Cached balances
        self._last_fetched = 0  # ✅ Last fetch timestamp

    def get_account_balances(self, account_number: str, refresh: bool = False):
        """
        Fetches and caches the account balances. Automatically refreshes if cache is older than CACHE_EXPIRY.

        :param account_number: The Tastytrade account number.
        :param refresh: If True, forces an API refresh instead of using cached data.
        :return: Dictionary containing account balance details.
        """
        current_time = time.time()
        cache_age = current_time - self._last_fetched

        if self._balances is None or refresh or cache_age > self.CACHE_EXPIRY:
            logger.info(
                f"🔄 Fetching balances for account {account_number} (Refresh={refresh} | Cache Age={cache_age:.1f}s)"
            )
            endpoint = f"/accounts/{account_number}/balances"

            try:
                response = self.api_client.get(endpoint)
                self._balances = response.get("data", {})  # ✅ Cache results
                self._last_fetched = current_time  # ✅ Update timestamp
                logger.debug(f"📊 Balances received: {self._balances}")
            except Exception as e:
                logger.error(f"🚨 Failed to fetch balances for {account_number}: {e}")
                return {}

        return self._balances

    def get_net_liquidating_value(self, account_number: str, refresh: bool = False):
        """
        Retrieves the net liquidating value of the account.

        :param account_number: The Tastytrade account number.
        :param refresh: If True, forces an API refresh.
        :return: Float representing the net liquidating value.
        """
        value = float(
            self.get_account_balances(account_number, refresh).get(
                "net-liquidating-value", 0.0
            )
        )
        logger.info(f"💰 Net Liquidating Value: ${value:,.2f}")
        return value

    def get_cash_balance(self, account_number: str, refresh: bool = False):
        """
        Retrieves the available cash balance for an account.

        :param account_number: The Tastytrade account number.
        :param refresh: If True, forces an API refresh.
        :return: Float representing the cash balance.
        """
        value = float(
            self.get_account_balances(account_number, refresh).get("cash-balance", 0.0)
        )
        logger.info(f"💵 Cash Balance: ${value:,.2f}")
        return value

    def get_equity_buying_power(self, account_number: str, refresh: bool = False):
        """
        Retrieves the equity buying power of the account.

        :param account_number: The Tastytrade account number.
        :param refresh: If True, forces an API refresh.
        :return: Float representing the equity buying power.
        """
        value = float(
            self.get_account_balances(account_number, refresh).get(
                "equity-buying-power", 0.0
            )
        )
        logger.info(f"📈 Equity Buying Power: ${value:,.2f}")
        return value

    def get_derivative_buying_power(self, account_number: str, refresh: bool = False):
        """
        Retrieves the derivative (options) buying power of the account.

        :param account_number: The Tastytrade account number.
        :param refresh: If True, forces an API refresh.
        :return: Float representing derivative (options) buying power.
        """
        value = float(
            self.get_account_balances(account_number, refresh).get(
                "derivative-buying-power", 0.0
            )
        )
        logger.info(f"📊 Derivative Buying Power: ${value:,.2f}")
        return value

    def get_margin_equity(self, account_number: str, refresh: bool = False):
        """
        Retrieves the margin equity value of the account.

        :param account_number: The Tastytrade account number.
        :param refresh: If True, forces an API refresh.
        :return: Float representing margin equity.
        """
        value = float(
            self.get_account_balances(account_number, refresh).get("margin-equity", 0.0)
        )
        logger.info(f"⚖️ Margin Equity: ${value:,.2f}")
        return value

    def get_accounts(self):
        """
        Fetches all accounts associated with the authenticated user.

        :return: List of account objects or an empty list if none exist.
        """
        response = self.api_client.get("/customers/me/accounts")

        # Ensure the response format is correct before returning data
        if (
            isinstance(response, dict)
            and "data" in response
            and "items" in response["data"]
        ):
            return response["data"]["items"]  # ✅ Return list of account objects

        return []  # ✅ Return an empty list if response format is unexpected

    def get_account_details(self, account_number: str):
        """
        Retrieves detailed information about a specific account.

        :param account_number: The Tastytrade account number.
        :return: Dictionary containing account details.
        """
        endpoint = f"/accounts/{account_number}"
        response = self.api_client.get(endpoint)
        return response.get("data", {})

    def get_account_positions(self, account_number: str):
        """
        Retrieves all open positions for a specific account.

        :param account_number: The Tastytrade account number.
        :return: List of position objects.
        """
        endpoint = f"/accounts/{account_number}/positions"
        response = self.api_client.get(endpoint)
        return response.get("data", [])

    def get_account_orders(self, account_number: str):
        """
        Fetches all orders associated with a specific account.

        :param account_number: The Tastytrade account number.
        :return: List of order objects.
        """
        endpoint = f"/accounts/{account_number}/orders"
        response = self.api_client.get(endpoint)
        return response.get("data", [])

    def parse_accounts(self, response_json):
        """
        Extracts a list of account numbers from the Tastytrade API response.

        :param response_json: JSON response from the API.
        :return: List of account numbers or an empty list on failure.
        """
        try:
            return [acc["account"]["account-number"] for acc in response_json]
        except (KeyError, TypeError) as e:
            logging.error(f"Error parsing accounts: {e}")
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
            return account_numbers[account_order_number]  # ✅ Return the account number
        return None
