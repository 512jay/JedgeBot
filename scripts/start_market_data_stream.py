import asyncio
from log_setup import logger  # Importing the logging setup
from jedgebot.broker.tastytrade.tastytrade import TastyTradeClient


async def main():
    """Starts market data streaming using the refactored method."""
    logger.info("🚀 Initializing TastyTradeClient...")

    # Initialize client
    client = TastyTradeClient()

    try:
        # Start market data streaming
        await client.start_market_data_streaming()
    except asyncio.CancelledError:
        logger.info("✅ Market data streaming stopped cleanly.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Script interrupted by user.")
