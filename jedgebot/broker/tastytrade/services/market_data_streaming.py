import asyncio
import json
import websockets
from log_setup import logger


class MarketDataStreamer:
    """Handles real-time market data streaming via DXLink WebSocket."""

    def __init__(self, api_client):
        self.api_client = api_client
        self.quote_token = None
        self.dxlink_url = None
        self.ws = None

    async def fetch_quote_token(self):
        """Fetches a new quote token from TastyTrade API."""
        logger.info("🔍 Requesting new quote token from TastyTrade API...")

        try:
            response = await self.api_client.post("/api-quote-tokens", json={})
            logger.info(f"📡 API Response: {response}")  # ✅ Log raw API response

            self.quote_token = response["data"]["token"]
            self.dxlink_url = response["data"]["dxlink-url"]
            logger.info(f"✅ Retrieved new Quote Token: {self.quote_token[:10]}... (truncated)")
            logger.info(f"✅ DXLink WebSocket URL: {self.dxlink_url}")

        except Exception as e:
            logger.error(f"❌ Failed to fetch quote token: {e}", exc_info=True)

    async def validate_quote_token(self):
        """Validates the quote token by attempting a WebSocket connection."""
        if not self.dxlink_url or not self.quote_token:
            logger.error("❌ Missing DXLink URL or Quote Token!")
            return False

        try:
            async with websockets.connect(self.dxlink_url) as ws:
                self.ws = ws
                logger.info("✅ WebSocket Connected for Token Validation.")
                return True
        except Exception as e:
            logger.error(f"❌ Token validation failed: {e}", exc_info=True)
            return False

    async def connect(self):
        """Establishes a WebSocket connection to DXLink."""
        logger.info(f"🔌 Connecting to DXLink WebSocket at {self.dxlink_url}...")

        try:
            async with websockets.connect(self.dxlink_url) as ws:
                self.ws = ws  # ✅ Store WebSocket instance
                logger.info("✅ Connected to DXLink WebSocket.")
                await self.on_open()  # ✅ Send SETUP after connecting
                await self.listen()   # ✅ Start listening for messages

        except websockets.exceptions.InvalidURI as e:
            logger.error(f"❌ Invalid WebSocket URL: {e}")
        except websockets.exceptions.WebSocketException as e:
            logger.error(f"❌ WebSocket Error: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected WebSocket Connection Failure: {e}", exc_info=True)

    async def on_open(self):
        """Handles WebSocket connection open event."""
        logger.info("✅ WebSocket Connection Established. Sending SETUP request...")
        if not self.ws:
            logger.error("❌ WebSocket connection missing! Cannot send SETUP.")
            return
        await self.send_setup_request()

    async def send_setup_request(self):
        """Sends the initial SETUP message to DXLink."""
        setup_message = {
            "type": "SETUP",
            "channel": 0,
            "version": "0.1-DXF-JS/0.3.0",
            "keepaliveTimeout": 60,
            "acceptKeepaliveTimeout": 60
        }
        logger.info(f"📡 Sending SETUP Request: {setup_message}")  # ✅ Log message before sending
        await self.send_message(setup_message)

    async def send_message(self, message):
        """Sends a message via WebSocket."""
        if self.ws:
            await self.ws.send(json.dumps(message))
            logger.info(f"📡 Sent WebSocket Message: {message}")
        else:
            logger.error("❌ WebSocket is not connected!")

    async def listen(self):
        """Listens for incoming WebSocket messages."""
        try:
            async for message in self.ws:
                await self.on_message(message)
        except Exception as e:
            logger.error(f"❌ WebSocket listening error: {e}", exc_info=True)

    async def on_message(self, message):
        """Handles incoming messages from DXLink."""
        try:
            parsed_message = json.loads(message)
            logger.info(f"📡 RAW WebSocket Message Received: {parsed_message}")

            if parsed_message.get("type") == "SETUP":
                logger.info("✅ Received SETUP Response from DXLink.")

            elif parsed_message.get("type") == "AUTH_STATE":
                await self.handle_auth_state(parsed_message)

        except Exception as e:
            logger.error(f"❌ Error processing WebSocket message: {e}", exc_info=True)

    async def handle_auth_state(self, message):
        """Handles AUTH_STATE responses."""
        state = message.get("state")
        if state == "UNAUTHORIZED":
            logger.info("🔑 Received AUTH_STATE: UNAUTHORIZED. Sending AUTH request...")
            await self.send_auth_request()
        elif state == "AUTHORIZED":
            logger.info("✅ Received AUTH_STATE: AUTHORIZED.")

    async def send_auth_request(self):
        """Sends the AUTH request to DXLink."""
        auth_message = {
            "type": "AUTH",
            "channel": 0,
            "token": self.quote_token
        }
        logger.info(f"📡 Sending AUTH Request: {auth_message}")
        await self.send_message(auth_message)

    async def start_streaming(self):
        """Starts the market data WebSocket connection."""
        logger.info("📡 Starting DXLink market data streaming...")

        if not self.dxlink_url:
            logger.error("❌ DXLink URL is missing! Cannot connect.")
            return
        
        await self.connect()
