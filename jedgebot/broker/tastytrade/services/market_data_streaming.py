import asyncio
import json
from typing import Optional
from log_setup import logger
from .quote_token_manager import QuoteTokenManager


class MarketDataStreamer:
    def __init__(self, client):
        self.client = client  # TastyTradeClient instance
        self.ws = None
        self.authorized = False
        self.channel_id = 0
        self.symbols = []

        # Use QuoteTokenManager for handling token logic
        self.token_manager = QuoteTokenManager(client.api_client)
        self.quote_token = None
        self.dxlink_url = None

    async def get_api_quote_token(self):
        """Fetches or retrieves the quote token asynchronously."""
        self.quote_token, self.dxlink_url = await self.token_manager.get_quote_token()
        if not self.quote_token:
            logger.error("❌ Cannot proceed with streaming without a valid quote token.")
            return False
        return True

    async def start_streaming(self, symbols: Optional[list[str]] = None):
        """Main entry point for market data streaming."""
        if symbols:
            self.symbols.extend(symbols)
            logger.info(f"📡 Symbols to stream: {self.symbols}")

        if not self.symbols:
            logger.error("❌ No symbols provided for market data streaming.")
            raise ValueError("No symbols provided for market data streaming.")

        logger.info("🔍 Starting market data streaming flow...")

        # Fetch and validate the quote token using the token manager
        if not await self.get_api_quote_token():

            return

        await self.setup()
        await self.authorize()
        await self.channel_request()
        await self.feed_setup()
        await self.feed_subscription()
        await self.keep_alive()
        await self.listen()

    async def setup(self):
        """Handles initial setup, including fetching a valid quote token and connecting to the WebSocket."""
        logger.info("🔍 Setting up WebSocket connection...")
        self.client.dxlink_url = (
            self.dxlink_url
        )  # Ensure WebSocket URL is set in client
        await self.client.connect()


    async def authorize(self):
        """Sends an AUTH request to DXLink using the quote token."""
        if not self.quote_token:
            logger.error(
                "[MarketDataStreamer] ❌ Cannot authorize: No quote token available."
            )
            return

        auth_message = {
            "type": "AUTH",
            "channel": 0,
            "token": self.quote_token,
        }

        logger.info("[MarketDataStreamer] 🔑 Sending AUTH request...")
        await self.ws.send(json.dumps(auth_message))

    async def channel_request(self):
        """Requests a new channel for data streaming."""
        self.channel_id += 1
        request = {
            "type": "CHANNEL_REQUEST",
            "channel": self.channel_id,
            "service": "FEED",
            "parameters": {"contract": "AUTO"},
        }
        await self.client.send_ws_message(request)
        logger.info(f"📡 Requested channel {self.channel_id}")

    async def feed_setup(self):
        """Configures the feed with the necessary event fields."""
        setup_message = {
            "type": "FEED_SETUP",
            "channel": self.channel_id,
            "acceptAggregationPeriod": 0.1,
            "acceptDataFormat": "COMPACT",
            "acceptEventFields": {
                "Trade": ["eventType", "eventSymbol", "price", "dayVolume", "size"],
                "Quote": [
                    "eventType",
                    "eventSymbol",
                    "bidPrice",
                    "askPrice",
                    "bidSize",
                    "askSize",
                ],
            },
        }
        await self.client.send_ws_message(setup_message)
        logger.info(f"📡 Feed setup configured on channel {self.channel_id}")

    async def feed_subscription(self):
        """Subscribes to market data events for selected symbols."""
        if not self.symbols:
            logger.warning("⚠️ No symbols to subscribe to.")
            return

        subscription_message = {
            "type": "FEED_SUBSCRIPTION",
            "channel": self.channel_id,
            "reset": True,
            "add": [{"type": "Trade", "symbol": symbol} for symbol in self.symbols],
        }
        await self.client.send_ws_message(subscription_message)
        logger.info(
            f"📡 Subscribed to market data for: {self.symbols} on channel {self.channel_id}"
        )

    async def keep_alive(self):
        """Sends periodic keep-alive messages."""
        while True:
            await asyncio.sleep(30)
            keepalive_message = {"type": "KEEPALIVE", "channel": self.channel_id}
            await self.client.send_ws_message(keepalive_message)
            logger.info("📡 Sent KEEPALIVE message.")

    async def listen(self):
        """Listens for incoming WebSocket messages."""
        while True:
            try:
                message = await self.ws.recv()
                await self.on_message(message)
            except asyncio.CancelledError:
                logger.info("🛑 Market data streaming interrupted. Cleaning up...")
                await self.client.close_connection()
                break

    async def on_message(self, message):
        """Handles incoming WebSocket messages."""
        data = json.loads(message)
        msg_type = data.get("type")

        if msg_type == "AUTH_STATE":
            state = data.get("state")
            if state == "UNAUTHORIZED":
                logger.info(
                    "[MarketDataStreamer] 🔑 Received UNAUTHORIZED state. Sending AUTH request..."
                )
                await self.authorize()
            elif state == "AUTHORIZED":
                self.authorized = True
                logger.info("[MarketDataStreamer] ✅ WebSocket successfully AUTHORIZED.")
        elif msg_type == "KEEPALIVE":
            logger.info("[MarketDataStreamer] 📡 KEEPALIVE received. Sending response...")
            await self.keep_alive()
        elif msg_type == "ERROR":
            logger.error(f"[MarketDataStreamer] ❌ WebSocket Error: {data}")
