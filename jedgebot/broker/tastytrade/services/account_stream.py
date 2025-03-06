import asyncio
import websockets
import json
from jedgebot.broker.tastytrade.data_handler import TastyTradeDataHandler


class TastyTradeAccountStream:
    def __init__(self, websocket_url: str, auth_token: str):
        """Initialize the WebSocket client for Tastytrade account streaming."""
        self.websocket_url = websocket_url
        self.auth_token = auth_token
        self.data_handler = TastyTradeDataHandler()
        self.websocket = None
        self.connected = False

    async def connect(self):
        """Establish a connection to the Tastytrade WebSocket server."""
        try:
            self.websocket = await websockets.connect(
                self.websocket_url,
                extra_headers={"Authorization": f"Bearer {self.auth_token}"}
            )
            self.connected = True
            await self.subscribe()
            await self.receive_messages()
        except Exception as e:
            print(f"❌ WebSocket connection failed: {e}")
            self.connected = False

    async def subscribe(self):
        """Subscribe to account updates."""
        if self.websocket and self.connected:
            subscription_message = {
                "action": "subscribe",
                "type": "account-updates"
            }
            await self.websocket.send(json.dumps(subscription_message))

    async def receive_messages(self):
        """Listen for incoming messages and process them."""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                self.handle_stream_update(data)
        except websockets.exceptions.ConnectionClosed:
            print("⚠️ WebSocket connection closed, attempting to reconnect...")
            self.connected = False
            await asyncio.sleep(5)
            await self.connect()
        except Exception as e:
            print(f"❌ WebSocket error: {e}")

    def handle_stream_update(self, data: dict):
        """Process WebSocket data updates."""
        if "account-updates" in data:
            self.data_handler.update_data("account", data["account-updates"])
            print("✅ Account data updated:", data["account-updates"])

    async def close(self):
        """Close the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
