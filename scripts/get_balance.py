import requests  # ✅ Add missing import
from jedgebot.broker.tastytrade_broker import TastyTradeBroker

def main():
    """Run the balance retrieval process."""
    print("🚀 Script started!")  # ✅ Debugging print

    print(f"🔍 Token being used: {self.token}")


    # Initialize the broker
    tasty_broker = TastyTradeBroker()
    print("✅ Broker initialized!")  # ✅ Debugging print

    print(f"🔍 Token being used: {self.token}")


    # Fetch and print account balance
    print("🔍 Fetching account balance...")
    account_balance = tasty_broker.get_account_balance()

    if account_balance:
        print("💰 Account Balance:", account_balance)
    else:
        print("❌ Failed to retrieve account balance!")

# ✅ Ensure the script runs when executed directly
if __name__ == "__main__":
    main()


def get_account_balance(self):
    """Fetch account balance from TastyTrade by first retrieving the account number."""
    headers = {
        "Authorization": f"Bearer {self.token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    print("🔍 Fetching account list...")  # Debugging output

    # 🔍 Step 1: Get account number from `/customers/me/accounts`
    try:
        response = requests.get(f"{self.BASE_URL}/customers/me/accounts", headers=headers)
        print("📡 API Response:", response.status_code, response.text)  # Debugging output
        response.raise_for_status()
        accounts_data = response.json()

        # Extract the first account number (assuming you have one account)
        accounts = accounts_data.get("data", {}).get("items", [])
        if not accounts:
            print("❌ No accounts found!")
            return None
        
        account_number = accounts[0]["account"]["account-number"]
        print(f"✅ Found Account Number: {account_number}")

    except requests.RequestException as e:
        print(f"❌ Failed to fetch accounts: {e}")
        return None

    # 🔍 Step 2: Use account number to fetch balance from `/accounts/{account_number}/balances`
    print(f"🔍 Fetching balance for account: {account_number}")

    try:
        balance_url = f"{self.BASE_URL}/accounts/{account_number}/balances"
        response = requests.get(balance_url, headers=headers)
        print("📡 API Response:", response.status_code, response.text)  # Debugging output
        response.raise_for_status()
        balance_data = response.json()

        print("✅ Account Balance Retrieved:", balance_data)  # Print the full balance response
        return balance_data

    except requests.RequestException as e:
        print(f"❌ Failed to fetch account balance: {e}")
        return None
