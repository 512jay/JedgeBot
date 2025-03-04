import requests
from jedgebot.broker.tastytrade_broker import TastyTradeBroker

def main():
    """Authenticate and fetch customer information from TastyTrade."""
    print("🚀 Script started!")

    # Initialize the broker
    tasty_broker = TastyTradeBroker()
    print("✅ Broker initialized!")

    # Ensure authentication
    token = tasty_broker.authenticate()
    print(f"🔍 DEBUG: Full Token Sent -> {token}")  # ✅ Debugging print

    # Define headers for the request
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    # Fetch customer details
    url = f"{tasty_broker.BASE_URL}/customers/me"
    print(f"🔍 Fetching customer info from: {url}")

    try:
        response = requests.get(url, headers=headers)
        print("📡 API Response:", response.status_code, response.text)  # Debugging output
        response.raise_for_status()
        customer_info = response.json()
        print("✅ Customer Information Retrieved:", customer_info)
    except requests.RequestException as e:
        print(f"❌ Failed to fetch customer info: {e}")

if __name__ == "__main__":
    main()
