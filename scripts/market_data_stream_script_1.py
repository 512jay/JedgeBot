import asyncio
from jedgebot.broker.tastytrade.tastytrade import TastyTradeClient
from log_setup import logger

async def test_market_data_streaming():
    """Test script for MarketDataStreamer functionality using TastyTradeClient facade."""
    logger.info("🚀 Starting MarketDataStreamer test...")

    # ✅ Initialize TastyTradeClient (handles authentication)
    tasty_client = TastyTradeClient()

    try:
        # ✅ Fetch and validate a quote token
        logger.info("🔍 Fetching and validating quote token...")
        await tasty_client.market_data_streamer.fetch_quote_token()
        await tasty_client.market_data_streamer.validate_quote_token()

        # ✅ Start Market Data Streaming
        logger.info("📡 Starting market data streaming...")
        await tasty_client.start_market_data_streaming()  # ✅ This was missing!

        logger.info("⏳ Market data stream running. Press CTRL+C to exit.")
        await asyncio.sleep(300)  # Keep the stream running for 5 minutes

        logger.info("✅ Market Data Streaming Test Completed.")

    except Exception as e:
        logger.error(f"❌ Unhandled Exception: {e}", exc_info=True)  # ✅ Print full error

if __name__ == "__main__":
    asyncio.run(test_market_data_streaming())
