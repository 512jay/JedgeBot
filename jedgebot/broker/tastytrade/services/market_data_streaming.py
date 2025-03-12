import asyncio
import json
import random
from typing import Optional
from jedgebot.utils.logging import logger
from .quote_token_manager import QuoteTokenManager
import traceback
import websockets
from jedgebot.broker.tastytrade.data_handler import TastyTradeDataHandler


class MarketDataStreamer:
    def __init__(self, client):
        self.authorized = False
        self.symbols = []

        # Use QuoteTokenManager for handling token logic
        self.token_manager = QuoteTokenManager(client.api_client)
        self.quote_token = None

        self.client = client
        self.ws_url = "wss://tasty-openapi-ws.dxfeed.com/realtime"  # Default URL
        self.channel_id = 1  # ✅ Single channel for all assets
        self.ws = None  # WebSocket connection
        self.quote_token_manager = QuoteTokenManager(self.client)
        self.data_handler = TastyTradeDataHandler()
        self.connected = False
        self.feed_established = False

    async def get_api_quote_token(self):
        """Fetches or retrieves the quote token asynchronously."""
        self.quote_token, self.dxlink_url = await self.token_manager.get_quote_token()
        if not self.quote_token:
            logger.error(
                "❌ Cannot proceed with streaming without a valid quote token."
            )
            return False
        return True

    async def feed_setup(self):
        """Configures the feed with the necessary event fields."""
        setup_message = {
            "type": "FEED_SETUP",
            "channel": self.channel_id,
            "acceptAggregationPeriod": 0.1,
            "acceptDataFormat": "COMPACT",
            "acceptEventFields": {
                "Trade": [
                    "eventType",
                    "eventSymbol",
                    "price",
                    "dayVolume",
                    "size",
                ],
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
        await self.send_ws_message(setup_message)
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
        await self.send_ws_message(subscription_message)
        logger.info(
            f"📡 Subscribed to market data for: {self.symbols} on channel {self.channel_id}"
        )

    async def keep_alive(self):
        """Sends periodic keep-alive messages."""
        while True:
            await asyncio.sleep(30)
            keepalive_message = {
                "type": "KEEPALIVE",
                "channel": self.channel_id,
            }
            await self.send_ws_message(keepalive_message)
            logger.info("📡 Sent KEEPALIVE message.")

    async def start_streaming(self, symbols: Optional[list[str]] = None):
        """Main entry point for market data streaming."""
        try:
            if symbols:
                self.symbols.extend(symbols)
                logger.info(f"📡 Symbols to stream: {self.symbols}")

            if not self.symbols:
                logger.error("❌ No symbols provided for market data streaming.")
                raise ValueError("No symbols provided for market data streaming.")

            logger.info("🔍 Starting market data streaming flow...")

            # Fetch and validate the quote token using the token manager
            if not await self.get_api_quote_token():
                logger.error(
                    "❌ Cannot proceed with streaming without a valid quote token."
                )
                return

            # ✅ Ensure WebSocket is connected before sending AUTH
            if not await self.connect_websocket():
                logger.error("❌ WebSocket connection failed. Cannot proceed.")
                return

            await self.listen()

        except Exception as e:
            logger.error(f"❌ Unhandled Exception: {e}")
            logger.error(
                traceback.format_exc()
            )  # Prints full error traceback for debugging

    async def connect_websocket(self):
        """Establishes the WebSocket connection and sends SETUP."""
        logger.info(
            f"[MarketDataStreamer] 🌐 Connecting to DXLink WebSocket at {self.ws_url}..."
        )

        try:
            self.ws = await websockets.connect(self.ws_url)
            logger.info("[MarketDataStreamer] ✅ WebSocket connection established.")

            # ✅ Send SETUP message immediately after connecting
            setup_message = {
                "type": "SETUP",
                "channel": 0,
                "version": "0.1-DXF-JS/0.3.0",
                "keepaliveTimeout": 60,
                "acceptKeepaliveTimeout": 60,
            }
            await self.send_ws_message(setup_message)
            logger.info(
                "[MarketDataStreamer] 📤 Sent SETUP message after WebSocket connection."
            )

            return True
        except Exception as e:
            logger.error(f"[MarketDataStreamer] ❌ Failed to connect WebSocket: {e}")
            return False

    async def authorize(self):
        """Sends an AUTH request to DXLink using the quote token."""
        if not self.quote_token:
            logger.error(
                "[MarketDataStreamer] ❌ Cannot authorize: No quote token available."
            )
            return

        if not self.ws:  # ✅ Ensure WebSocket exists before sending
            logger.error(
                "[MarketDataStreamer] ❌ Cannot authorize: WebSocket connection is missing."
            )
            return

        auth_message = {
            "type": "AUTH",
            "channel": 0,
            "token": self.quote_token,
        }

        logger.info("[MarketDataStreamer] 🔑 Sending AUTH request...")
        await self.ws.send(json.dumps(auth_message))

    async def send_ws_message(self, message):
        """Sends a WebSocket message."""
        if self.ws:
            try:
                await self.ws.send(json.dumps(message))
                logger.info(f"📤 Sent WebSocket message: {message}")
            except Exception as e:
                logger.error(f"❌ Failed to send WebSocket message: {e}")

    async def channel_request(self):
        """Requests a single market data channel for all asset types."""
        request = {
            "type": "CHANNEL_REQUEST",
            "channel": self.channel_id,
            "service": "FEED",
            "parameters": {"contract": "AUTO"},
        }
        await self.send_ws_message(request)
        logger.info(f"📡 Opened single market data channel {self.channel_id}")

    async def handle_websocket_message(self, message):
        """Handles incoming WebSocket messages from DXLink."""
        try:
            data = json.loads(message)
            logger.info(f"[MarketDataStreamer] 🔄 Received WebSocket Message: {data}")

            msg_type = data.get("type")
            channel = data.get("channel")

            if msg_type == "AUTH_STATE" and data.get("state") == "UNAUTHORIZED":
                self.authorized = False
                await self.authorize()
            elif msg_type == "AUTH_STATE" and data.get("state") == "AUTHORIZED":
                self.authorized = True
                await self.channel_request()
            elif msg_type == "CHANNEL_OPENED":
                self.feed_established = True
                await self.feed_setup()
            elif msg_type == "FEED_CONFIG":
                await self.feed_subscription()
            elif msg_type == "SETUP":
                logger.info(f"[MarketDataStreamer] ✅ SETUP complete")
            elif msg_type == "KEEPALIVE":
                logger.info(
                    f"[MarketDataStreamer] 🔄 Received KEEPALIVE for channel {channel}, responding..."
                )
                await self.send_ws_message({"type": "KEEPALIVE", "channel": channel})
            elif msg_type in ["Trade", "Quote"]:
                self.data_handler.update_data(msg_type, data)
                logger.info(f"✅ Processed market data update: {data}")
            else:
                logger.debug(f"ℹ️ Unhandled WebSocket Message: {data}")

        except Exception as e:
            logger.error(f"❌ Failed to process WebSocket message: {e}")

    async def listen(self):
        """Listens for incoming WebSocket messages."""
        logger.info("[MarketDataStreamer] 🎧 Listening for WebSocket messages...")
        try:
            async for message in self.ws:
                await self.handle_websocket_message(message)
        except websockets.exceptions.ConnectionClosed as e:
            logger.warning(f"[MarketDataStreamer] ⚠️ WebSocket connection lost: {e}")
            self.connected = False
            await self.reconnect()

    async def reconnect(self):
        delay = 2  # Initial delay
        while True:
            try:
                logger.info("🔄 Reconnecting WebSocket...")
                if await self.connect_websocket():
                    await self.authorize()
                    await self.feed_subscription()
                    return
            except Exception as e:
                logger.warning(f"Reconnect failed: {e}")

            delay = min(delay * 2, 60)  # Exponential backoff (max 60s)
            await asyncio.sleep(
                delay + random.uniform(0, 1)
            )  # Jitter to prevent sync issues
