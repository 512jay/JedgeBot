import json
import os
import time
import websockets
from jedgebot.utils.logging import logger

# Path to store both session and quote tokens
TOKEN_STORAGE_PATH = os.path.expanduser("~") + "/AppData/Roaming/tastytrade_tokens.json"


class QuoteTokenManager:
    """Handles fetching, validating, storing, and retrieving the Tastytrade quote token."""

    def __init__(self, api_client):
        """Initializes the QuoteTokenManager with an API client."""
        self.api_client = api_client
        self.quote_token = None
        self.dxlink_url = None

    def load_tokens(self):
        """Loads stored tokens (session + quote) from the JSON file."""
        if not os.path.exists(TOKEN_STORAGE_PATH):
            return {}

        try:
            with open(TOKEN_STORAGE_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error(
                "[QuoteTokenManager] ❌ Token JSON file is corrupted! Deleting it."
            )
            os.remove(TOKEN_STORAGE_PATH)
            return {}
        except Exception as e:
            logger.error(f"[QuoteTokenManager] ❌ Failed to load tokens JSON: {e}")
            return {}

    def save_tokens(self, updated_data):
        """Saves updated token data (session + quote) to the JSON file, creating a backup first."""
        try:
            if os.path.exists(TOKEN_STORAGE_PATH):
                os.rename(TOKEN_STORAGE_PATH, TOKEN_STORAGE_PATH + ".backup")

            with open(TOKEN_STORAGE_PATH, "w") as f:
                json.dump(updated_data, f, indent=4)

            logger.info(
                "[QuoteTokenManager] 💾 Tokens (session + quote) saved to JSON."
            )

            if os.path.exists(TOKEN_STORAGE_PATH + ".backup"):
                os.remove(TOKEN_STORAGE_PATH + ".backup")

        except Exception as e:
            logger.error(f"[QuoteTokenManager] ❌ Failed to save tokens JSON: {e}")
            if os.path.exists(TOKEN_STORAGE_PATH + ".backup"):
                logger.warning("[QuoteTokenManager] ⚠️ Restoring backup token file.")
                os.rename(TOKEN_STORAGE_PATH + ".backup", TOKEN_STORAGE_PATH)

    async def test_dxlink_connection(self, token_data):
        """Tests if the quote token is valid by sending a SETUP message to DXLink."""
        if (
            not token_data
            or "quote_token" not in token_data
            or "dxlink_url" not in token_data
        ):
            return False

        uri = token_data["dxlink_url"]

        try:
            async with websockets.connect(uri) as ws:
                setup_message = {
                    "type": "SETUP",
                    "channel": 0,
                    "version": "0.1-DXF-JS/0.3.0",
                    "keepaliveTimeout": 60,
                    "acceptKeepaliveTimeout": 60,
                    "authToken": token_data["quote_token"],
                }
                await ws.send(json.dumps(setup_message))

                response = await ws.recv()
                response_data = json.loads(response)

                logger.info(f"[QuoteTokenManager] 🔍 DXLink Response: {response_data}")

                if response_data.get("type") == "SETUP":
                    logger.info(
                        "[QuoteTokenManager] ✅ Quote token is valid (DXLink responded)."
                    )
                    return True

                logger.warning(
                    "[QuoteTokenManager] ⚠️ DXLink did not respond correctly to SETUP."
                )
                return False

        except Exception as e:
            logger.warning(f"[QuoteTokenManager] ❌ Failed to test quote token: {e}")
            return False

    async def is_token_valid(self, token_data):
        """Checks if the stored quote token is still valid using timestamp and a DXLink test."""
        if not token_data:
            return False

        issued_time = token_data.get("quote_token_timestamp", 0)
        current_time = time.time()
        expires_in = 24 * 60 * 60  # 24 hours
        refresh_threshold = expires_in - (60 * 60)  # Refresh 1 hour before expiry

        if current_time - issued_time < refresh_threshold:
            logger.info(
                "[QuoteTokenManager] ✅ Cached quote token timestamp looks valid."
            )
            return await self.test_dxlink_connection(token_data)

        logger.warning(
            "[QuoteTokenManager] ⚠️ Cached quote token is nearing expiration. Refreshing..."
        )
        return False

    def fetch_new_token(self):
        """Fetches a new quote token from Tastytrade API with a retry mechanism."""
        logger.info(
            "[QuoteTokenManager] 🔍 Fetching API Quote Token from Tastytrade..."
        )
        response = self.api_client.get("/api-quote-tokens")

        if response and "data" in response:
            token_data = self.load_tokens()
            token_data["quote_token"] = response["data"]["token"]
            token_data["dxlink_url"] = response["data"]["dxlink-url"]
            token_data["quote_token_timestamp"] = time.time()

            self.save_tokens(token_data)
            return response["data"]

        logger.error(
            "[QuoteTokenManager] ❌ Failed to fetch quote token. Retrying once..."
        )
        time.sleep(2)

        response = self.api_client.get("/api-quote-tokens")
        if response and "data" in response:
            token_data = self.load_tokens()
            token_data["quote_token"] = response["data"]["token"]
            token_data["dxlink_url"] = response["data"]["dxlink-url"]
            token_data["quote_token_timestamp"] = time.time()

            self.save_tokens(token_data)
            return response["data"]

        logger.critical(
            "[QuoteTokenManager] 🚨 Fetching quote token failed after retry. Check API connection!"
        )
        return None

    async def get_quote_token(self):
        """Gets the quote token from cache or fetches a new one if expired or invalid."""
        token_data = self.load_tokens()

        if await self.is_token_valid(token_data):
            self.quote_token = token_data["quote_token"]
            self.dxlink_url = token_data["dxlink_url"]
            logger.info("[QuoteTokenManager] 🚀 Using cached quote token.")
            return self.quote_token, self.dxlink_url

        logger.info(
            "[QuoteTokenManager] 🔄 Cached token expired or failed DXLink test, fetching a new one..."
        )
        token_data = self.fetch_new_token()

        if token_data:
            self.quote_token = token_data["token"]
            self.dxlink_url = token_data["dxlink-url"]
            logger.info("[QuoteTokenManager] 🚀 Fetched and stored a new quote token.")
            return self.quote_token, self.dxlink_url

        logger.error("[QuoteTokenManager] ❌ Failed to retrieve a valid quote token.")
        return None, None
