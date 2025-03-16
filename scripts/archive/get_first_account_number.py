import os

from dotenv import load_dotenv

from backend.broker.tastytrade.tastytrade import TastyTradeClient
from log_setup import logger

# Load environment variables
load_dotenv()

# Get login credentials from .env
USERNAME = os.getenv("TASTYTRADE_USERNAME")
PASSWORD = os.getenv("TASTYTRADE_PASSWORD")


def main():
    logger.info("🔍 Logging initialized")

    if not USERNAME or not PASSWORD:
        logger.error("❌ Username or password is missing in the .env file")
        return

    try:
        # Initialize TastytradeClient
        tasty = TastyTradeClient(USERNAME, PASSWORD)
        first_account = tasty.get_account_number()

        if first_account:
            logger.info(f"✅ Retrieved First Account: {first_account}")
            print(f"✅ First Account Number: {first_account}")
        else:
            logger.warning("⚠️ No accounts found.")

    except Exception as e:
        logger.exception(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
