import asyncio
import websockets
import json
from jedgebot.broker.tastytrade.data_handler import TastyTradeDataHandler
from jedgebot.utils.logging import logger


class TastyTradeAccountStream:
    """Handles real-time account streaming from Tastytrade's WebSocket."""

    STREAM_URL = "wss://streamer.tastyworks.com"  # ✅ Using Production WebSocket
    HEARTBEAT_INTERVAL = 30  # ✅ Send heartbeat every 30 seconds

    def __init__(self, tasty_client):
        """
        Initialize the WebSocket client for Tastytrade account streaming.

        :param tasty_client: An instance of TastyTradeClient to provide authentication and account details.
        """
        self.tasty_client = tasty_client  # ✅ Use the passed-in client
        self.auth_token = (
            self.tasty_client.auth.get_session_token()
        )  # ✅ Fetch session token from the shared client
        self.account_number = (
            self.tasty_client.get_account_number()
        )  # ✅ Fetch account number from the shared client

        self.websocket_url = self.STREAM_URL
        self.data_handler = TastyTradeDataHandler()
        self.websocket = None
        self.connected = False

    async def connect(self):
        """Establish a connection to the Tastytrade WebSocket server."""
        try:
            logger.info(f"🔍 Connecting to WebSocket URL: {self.websocket_url}")
            logger.info(
                f"🔑 Using Auth Token: {self.auth_token[:10]}... (truncated for security)"
            )

            self.websocket = await websockets.connect(
                self.websocket_url
            )  # ✅ No headers

            self.connected = True
            logger.info("✅ WebSocket Connection Established")

            # Send initial messages like `on_open()`
            await self.on_open()

            # Start receiving messages
            await self.receive_messages()
        except Exception as e:
            logger.error(f"❌ WebSocket connection failed: {e}")
            self.connected = False
            await asyncio.sleep(5)
            await self.connect()  # ✅ Auto-reconnect logic

    async def on_open(self):
        """Subscribes to account updates in the correct order."""
        logger.info(f"✅ Subscribing to account updates for: {self.account_number}")

        # ✅ Step 1: Send `connect` FIRST
        await self.send_message("connect", value=[self.account_number], request_id=2)

        # ✅ Step 2: Small delay to ensure `connect` is acknowledged
        await asyncio.sleep(1)

        # ✅ Step 3: Subscribe to additional notifications
        await self.send_message("public-watchlists-subscribe", request_id=3)
        await self.send_message("quote-alerts-subscribe", request_id=4)
        await self.send_message("user-message-subscribe", request_id=5)

        # ✅ Step 4: Start sending heartbeats
        asyncio.create_task(self.send_heartbeats())

    async def send_message(self, action, value=None, request_id=None):
        """Sends a formatted WebSocket message including `auth-token`."""
        if not self.websocket:
            logger.error("⚠️ WebSocket is not connected.")
            return

        message = {
            "action": action,
            "auth-token": self.auth_token,  # ✅ Required for every WebSocket request
        }

        if value:
            message["value"] = value  # ✅ Include optional value if needed
        if request_id is not None:
            message["request-id"] = request_id  # ✅ Include request ID for tracking

        await self.websocket.send(json.dumps(message))
        logger.info(f"📡 Sent WebSocket Message: {message}")

    async def receive_messages(self):
        """Listen for incoming messages and process them."""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                logger.info(f"📡 WebSocket Message: {data}")

                # ✅ Capture session ID if available
                if data.get("action") == "connect" and data.get("status") == "ok":
                    self.web_socket_session_id = data.get("web-socket-session-id")

                # Process other data
                self.handle_stream_update(data)

        except websockets.exceptions.ConnectionClosed:
            logger.warning("⚠️ WebSocket connection closed, attempting to reconnect...")
            self.connected = False
            await asyncio.sleep(5)
            await self.connect()
        except Exception as e:
            logger.error(f"❌ WebSocket error: {e}")

    def handle_stream_update(self, data: dict):
        """Process WebSocket data updates."""
        if "account-updates" in data:
            self.data_handler.update_data("account", data["account-updates"])
            logger.info(f"✅ Account data updated: {data['account-updates']}")

    async def send_heartbeats(self):
        """Sends heartbeat messages periodically to keep the connection alive."""
        while self.connected:
            await asyncio.sleep(self.HEARTBEAT_INTERVAL)
            await self.send_message("heartbeat", request_id=1)
            logger.info("❤️ Sent WebSocket Heartbeat")

    async def close(self):
        """Close the WebSocket connection."""
        self.connected = False
        if self.websocket:
            await self.websocket.close()
            logger.info("🔌 WebSocket Connection Closed")
