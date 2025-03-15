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
    logger.info("📊 Fetching account balances...")

    if not USERNAME or not PASSWORD:
        logger.error("❌ Username or password is missing in the .env file")
        return

    try:
        # ✅ Initialize TastyTradeClient (Handles authentication & API client)
        tasty = TastyTradeClient(USERNAME, PASSWORD)

        # ✅ Get the first account number
        account_number = tasty.get_account_number()
        if not account_number:
            logger.warning("⚠️ No accounts found. Exiting.")
            return

        logger.info(f"✅ Using Account: {account_number}")

        # ✅ Fetch balances using `tasty.account`
        balances = tasty.account.get_account_balances(account_number)

        print("\n--- Account Balances ---")
        print(
            f"Net Liquidating Value: ${tasty.account.get_net_liquidating_value(account_number):,.2f}"
        )
        print(f"Cash Balance: ${tasty.account.get_cash_balance(account_number):,.2f}")
        print(
            f"Equity Buying Power: ${tasty.account.get_equity_buying_power(account_number):,.2f}"
        )
        print(
            f"Derivative Buying Power: ${tasty.account.get_derivative_buying_power(account_number):,.2f}"
        )
        print(f"Margin Equity: ${tasty.account.get_margin_equity(account_number):,.2f}")

        logger.info("✅ Balances displayed successfully.")

    except Exception as e:
        logger.exception(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
