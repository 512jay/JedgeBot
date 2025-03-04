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

    # Fetch accounts using AccountService
    
    client = TastyTradeClient(username, password)

    # Fetch accounts
    account_service = client.account_service
    accounts = account_service.get_accounts()

    # Print first account number
    if accounts:
        print(f"First Account Number: {accounts[0]}")
    else:
        print("No accounts found.")

if __name__ == "__main__":
    main()
