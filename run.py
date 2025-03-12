import os
from jedgebot.utils.logging import logger
from dotenv import load_dotenv
from jedgebot.broker.tastytrade.tastytrade import TastyTradeClient

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
        tasty = TastytradeClient(USERNAME, PASSWORD)
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
