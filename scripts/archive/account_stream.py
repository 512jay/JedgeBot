import json
import websocket
import threading
import time
from jedgebot.broker.tastytrade.tastytrade import TastyTradeClient
from log_setup import logger


class TastyTradeAccountStreamer:
    """Handles real-time account streaming from Tastytrade's WebSocket."""

    STREAM_URL = "wss://streamer.tastyworks.com"  # ✅ Using Production WebSocket
    HEARTBEAT_INTERVAL = 30  # ✅ Send heartbeat every 30 seconds

    def __init__(self, tasty_client: TastyTradeClient):
        """
        Initialize the account streaming WebSocket.

        :param tasty_client: Instance of an already authenticated TastyTradeClient.
        """
        self.tasty_client = tasty_client  # ✅ Reuse external client
        self.ws = None
        self.should_reconnect = True  # ✅ Enables automatic reconnection
        self.web_socket_session_id = None  # ✅ Store session ID for tracking

    def send_message(self, action, value=None, request_id=None):
        """Sends a formatted WebSocket message including `auth-token`."""
        session_token = self.tasty_client.auth.get_session_token()

        message = {
            "action": action,
            "auth-token": session_token,  # ✅ Required for every WebSocket request
        }

        if value:
            message["value"] = value  # ✅ Include optional value if needed
        if request_id is not None:
            message["request-id"] = request_id  # ✅ Include request ID for tracking

        self.ws.send(json.dumps(message))
        logger.info(f"📡 Sent WebSocket Message: {message}")

    def on_message(self, ws, message):
        """Handles incoming WebSocket messages."""
        data = json.loads(message)
        logger.info(f"📡 WebSocket Message: {data}")

        # ✅ Capture session ID if available
        if data.get("action") == "connect" and data.get("status") == "ok":
            self.web_socket_session_id = data.get("web-socket-session-id")

    def on_error(self, ws, error):
        """Handles WebSocket errors."""
        logger.error(f"🚨 WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """Handles WebSocket disconnections and attempts to reconnect."""
        logger.warning(f"🔌 WebSocket Closed: {close_status_code} - {close_msg}")

        if self.should_reconnect:
            logger.info("♻️ Reconnecting in 5 seconds...")
            time.sleep(5)
            self.start()  # ✅ Reconnects automatically

    def on_open(self, ws):
        """Subscribes to account updates in the correct order."""
        logger.info("✅ WebSocket Connection Established")

        # ✅ Step 1: Get the first account number
        account_number = self.tasty_client.get_account_number()

        if not account_number:
            logger.warning("⚠️ No valid accounts found. Exiting.")
            return

        logger.info(f"✅ Subscribing to account updates for: {account_number}")

        # ✅ Step 2: Send `connect` FIRST before anything else
        self.send_message("connect", value=[account_number], request_id=2)

        # ✅ Step 3: Wait to ensure `connect` is acknowledged
        time.sleep(1)

        # ✅ Step 4: Subscribe to additional notifications
        self.send_message("public-watchlists-subscribe", request_id=3)
        self.send_message("quote-alerts-subscribe", request_id=4)
        self.send_message("user-message-subscribe", request_id=5)

        # ✅ Step 5: Start sending heartbeats in a separate thread
        heartbeat_thread = threading.Thread(target=self.send_heartbeats, daemon=True)
        heartbeat_thread.start()
        logger.info("❤️ Heartbeat thread started.")

    def send_heartbeats(self):
        """Sends heartbeat messages periodically to keep the connection alive."""
        while self.should_reconnect:
            time.sleep(self.HEARTBEAT_INTERVAL)
            self.send_message("heartbeat", request_id=1)

    def start(self):
        """Starts the WebSocket connection in a separate thread."""
        self.ws = websocket.WebSocketApp(
            self.STREAM_URL,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        thread.start()
        logger.info("🚀 WebSocket Listener Started")

    def stop(self):
        """Stops the WebSocket connection."""
        self.should_reconnect = False  # ✅ Disable reconnections
        if self.ws:
            self.ws.close()
            logger.info("🔌 WebSocket Connection Closed")


if __name__ == "__main__":
    # ✅ Create a single instance of TastyTradeClient
    tasty_client = TastyTradeClient()

    # ✅ Pass the client to TastyTradeAccountStreamer
    streamer = TastyTradeAccountStreamer(tasty_client)
    streamer.start()

    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Stopping WebSocket...")
        streamer.stop()
