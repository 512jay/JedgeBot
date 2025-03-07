import asyncio
import json
import websockets
from log_setup import logger


class MarketDataStreamer:
    """Handles real-time market data streaming via DXLink WebSocket."""

    def __init__(self, client):
        self.client = client  # Store the entire TastyTradeClient instance
        self.api_client = client.api_client
        self.auth = client.auth
        self.quote_token = None
        self.dxlink_url = None
        self.ws = None

    async def fetch_quote_token(self):
        """Fetches a new quote token from TastyTrade API."""
        logger.info("🔍 Requesting new quote token from TastyTrade API...")
        try:
            response = self.api_client.get("/api-quote-tokens")
            logger.info(f"📡 API Response: {response}")
            self.quote_token = response["data"]["token"]
            self.dxlink_url = response["data"]["dxlink-url"]
        except Exception as e:
            logger.error(f"❌ Failed to fetch quote token: {e}", exc_info=True)

    async def connect(self):
        """Establishes a WebSocket connection to DXLink."""
        logger.info(f"🔌 Connecting to DXLink WebSocket at {self.dxlink_url}...")
        try:
            async with websockets.connect(self.dxlink_url) as ws:
                self.ws = ws
                logger.info("✅ Connected to DXLink WebSocket.")
                await self.send_setup_request()
                await self.listen()
        except Exception as e:
            logger.error(f"❌ WebSocket Connection Failure: {e}", exc_info=True)

    async def send_setup_request(self):
        """Sends the initial SETUP message to DXLink."""
        setup_message = {
            "type": "SETUP",
            "channel": 0,
            "version": "0.1-DXF-JS/0.3.0",
            "keepaliveTimeout": 60,
            "acceptKeepaliveTimeout": 60,
        }
        await self.send_message(setup_message)

    async def send_message(self, message):
        """Sends a message via WebSocket."""
        if self.ws:
            await self.ws.send(json.dumps(message))
        else:
            logger.error("❌ WebSocket is not connected!")

    async def handle_message(self, message):
        """Processes incoming WebSocket messages."""
        logger.info(f"📡 RAW WebSocket Message Received: {message}")
        try:
            message_data = json.loads(message)
            message_type = message_data.get("type")

            if message_type == "KEEPALIVE":
                logger.info("💓 Received KEEPALIVE from DXLink.")
            elif message_type == "ERROR":
                logger.error(f"❌ DXLink Error: {message_data.get('message')}")
            elif message_type == "AUTH_STATE":
                await self.handle_auth_state(message_data)
        except json.JSONDecodeError:
            logger.error(f"❌ Failed to parse WebSocket message: {message}")

    async def handle_auth_state(self, message):
        """Handles AUTH_STATE responses."""
        state = message.get("state")
        if state == "UNAUTHORIZED":
            logger.info("🔑 Received AUTH_STATE: UNAUTHORIZED. Sending AUTH request...")
            await self.send_auth_request()
        elif state == "AUTHORIZED":
            logger.info("✅ Received AUTH_STATE: AUTHORIZED.")
            asyncio.create_task(self.send_keepalive())

    async def send_auth_request(self):
        """Sends the AUTH request to DXLink."""
        auth_message = {"type": "AUTH", "channel": 0, "token": self.quote_token}
        await self.send_message(auth_message)

    async def send_keepalive(self):
        """Sends periodic keepalive messages to DXLink to prevent timeout."""
        try:
            while True:
                await asyncio.sleep(30)
                if self.ws:
                    keepalive_message = {"type": "KEEPALIVE", "channel": 0}
                    await self.send_message(keepalive_message)
        except asyncio.CancelledError:
            logger.info("🛑 Keepalive task cancelled.")

    async def listen(self):
        """Listens for incoming WebSocket messages."""
        try:
            while True:
                message = await self.ws.recv()
                await self.handle_message(message)
        except websockets.exceptions.ConnectionClosed:
            logger.warning("⚠️ WebSocket connection closed unexpectedly.")
        except Exception as e:
            logger.error(f"❌ Error in WebSocket listener: {e}", exc_info=True)
