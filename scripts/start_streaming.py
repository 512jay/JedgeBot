import asyncio
import traceback
from jedgebot.broker.tastytrade.tastytrade import TastyTradeClient
from log_setup import logger

# Setup logging
logger.info("Initializing TastyTradeClient...")

async def main():
    try:
        # Initialize TastyTradeClient
        tasty_client = TastyTradeClient()

        # Start account streaming
        logger.info("Starting WebSocket streaming for account updates...")
        tasty_client.start_account_stream()
        logger.info("Streaming started successfully.")

        # ✅ Keep the connection alive for a few heartbeats
        heartbeat_duration = 90  # Keep alive for ~3 heartbeats (30s interval)
        logger.info(f"💓 Keeping connection alive for {heartbeat_duration} seconds...")
        await asyncio.sleep(heartbeat_duration)

    except Exception as e:
        logger.error("Unhandled Exception during streaming.")
        logger.error(f"Exception: {e}")
        logger.error(traceback.format_exc())

    finally:
        # Ensure clean shutdown
        logger.info("Attempting to stop WebSocket streaming...")
        try:
            tasty_client.stop_account_stream()
            logger.info("WebSocket streaming stopped.")
        except Exception as stop_error:
            logger.error("Error while stopping streaming.")
            logger.error(f"Exception: {stop_error}")
            logger.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())
