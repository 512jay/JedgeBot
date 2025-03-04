def main():
    import os

    from dotenv import load_dotenv

    from jedgebot.broker.tastytrade.tastytrade_client import TastyTradeClient

    # Load environment variables
    load_dotenv()

    username = os.getenv("TASTYTRADE_USERNAME")
    password = os.getenv("TASTYTRADE_PASSWORD")

    if not username or not password:
        raise ValueError(
            "TASTYTRADE_USERNAME and TASTYTRADE_PASSWORD must be set in .env file"
        )

    # Initialize broker
    broker = TastyTradeClient(username, password)
    accounts = broker.extract_account_numbers()
    print(accounts)
    print("Closing without logging out...")


if __name__ == "__main__":
    main()
