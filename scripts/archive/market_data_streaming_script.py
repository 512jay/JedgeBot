import asyncio
from jedgebot.broker.tastytrade.services.market_data_streaming import MarketDataStreamer
from jedgebot.broker.tastytrade.tastytrade import TastyTradeClient
from log_setup import logger

async def test_market_data_streaming():
    """Test script for MarketDataStreamer functionality using TastyTradeClient facade."""
    logger.info("🚀 Starting MarketDataStreamer test...")
    
    # ✅ Initialize TastyTradeClient (handles authentication)
    tasty_client = TastyTradeClient()
    
    # ✅ Create MarketDataStreamer instance
    market_data_streamer = MarketDataStreamer(tasty_client.auth)
    
    # ✅ Test fetching a quote token
    logger.info("🔍 Fetching quote token...")
    token, dxlink_url = await market_data_streamer.fetch_quote_token()
    if token and dxlink_url:
        logger.info(f"✅ Quote Token: {token[:10]}... (truncated)")
        logger.info(f"✅ DXLink URL: {dxlink_url}")
    else:
        logger.error("❌ Failed to retrieve quote token.")
        return
    
    # ✅ Test validation of the fetched token
    logger.info("🔍 Validating fetched token...")
    is_valid = await market_data_streamer.validate_quote_token()
    if is_valid:
        logger.info("✅ Token validation successful.")
    else:
        logger.error("❌ Token validation failed.")
    
    # ✅ Run the automatic token monitor for 5 minutes (for testing)
    logger.info("⏳ Starting token monitoring (will run for 5 minutes)...")
    monitor_task = asyncio.create_task(market_data_streamer.monitor_token_expiry())
    await asyncio.sleep(300)  # Keep monitoring for 5 minutes
    monitor_task.cancel()  # Stop monitoring after test
    
    logger.info("✅ MarketDataStreamer test completed successfully.")

if __name__ == "__main__":
    asyncio.run(test_market_data_streaming())