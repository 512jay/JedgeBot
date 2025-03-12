import os
from jedgebot.utils.logging import logger


TOKEN_FILE = os.path.expanduser("~") + "/AppData/Roaming/tastytrade_tokens.json"


def stop_streaming_services(client):
    """Stops account and market data streaming services."""
    if client.account_stream:
        logger.info("📡 Stopping account streaming...")
        client.stop_account_stream()

    if hasattr(client, "market_data_streamer"):
        logger.info("📡 Stopping market data streaming...")
        client.market_data_streamer.stop_streaming()


def logout(client, clear_session=False):
    """
    Logs out of TastyTrade, stops streams, and optionally clears session tokens.

    :param client: TastyTradeClient instance
    :param clear_session: If True, removes the session token (forces full re-login).
    """
    logger.info("🚪 Logging out of TastyTrade...")

    # ✅ Stop streaming services
    stop_streaming_services(client)

    # ❌ Preserve session token by default
    if clear_session and os.path.exists(TOKEN_FILE):
        logger.info("🗑️ Clearing saved authentication tokens...")
        os.remove(TOKEN_FILE)

    logger.info(
        f"✅ Logout complete. {'Session token cleared.' if clear_session else 'Session token preserved.'}"
    )
