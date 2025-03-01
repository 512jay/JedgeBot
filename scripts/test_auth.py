import requests
import os
from dotenv import load_dotenv

# Explicitly load .env from jedgebot/
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "jedgebot", ".env")
load_dotenv(dotenv_path)

# Select API environment
ENV = os.getenv("TASTYTRADE_ENV", "live").lower()
BASE_URL = "https://api.tastytrade.com" if ENV == "live" else "https://api.cert.tastytrade.com"

# Get the correct credentials
username = os.getenv("TASTYTRADE_PAPER_USERNAME") if ENV == "paper" else os.getenv("TASTYTRADE_USERNAME")
password = os.getenv("TASTYTRADE_PAPER_PASSWORD") if ENV == "paper" else os.getenv("TASTYTRADE_PASSWORD")

# API endpoint
url = f"{BASE_URL}/sessions"

# Headers
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Request payload
data = {
    "login": username,
    "password": password
}

print(f"Attempting authentication on {ENV.upper()} environment...")
response = requests.post(url, json=data, headers=headers)

print("\nStatus Code:", response.status_code)
print("Response JSON:", response.json())