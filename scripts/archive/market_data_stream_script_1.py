import asyncio
from log_setup import logger
from backend.broker.tastytrade.tastytrade import TastyTradeClient


async def test_market_data_streaming():
    """Test script to start market data streaming without exit handling."""
    logger.info("🚀 Initializing TastyTradeClient...")

    # Initialize client
    client = TastyTradeClient()

    # Start streaming
    await client.start_market_data_streaming()


if __name__ == "__main__":
    asyncio.run(test_market_data_streaming())
