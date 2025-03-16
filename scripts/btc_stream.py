import asyncio
from backend.broker.tastytrade.tastytrade import TastyTradeClient
from backend.utils.logging import logger


async def main():
    """Starts the market data streaming for BTC."""
    # BTC/USD:CXTALP
    client = TastyTradeClient()
    print("🚀 Starting market data streaming for BTC...")
    await client.start_market_data_streaming(symbols=["BTC/USD:CXTALP"])


if __name__ == "__main__":
    asyncio.run(main())
