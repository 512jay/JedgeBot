import datetime
import json
import os
import platform
import time

import requests


class Authentication:
    BASE_URL = "https://api.tastyworks.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.remember_token = None
        self.session_token = None
        self.session_expiration = None
        self.password_used = False  # Track if password login was used
        self.token_file = self._get_token_file_path()
        self._load_tokens()
        self.ensure_authenticated()  # Ensure authentication on initialization

    def _get_token_file_path(self):
        """Determine the appropriate token storage path based on OS and username."""
        if platform.system() == "Windows":
            base_dir = os.path.join(os.getenv("APPDATA"), "jedgebot", self.username)
        else:  # Linux/Mac
            base_dir = os.path.join(
                os.path.expanduser("~"), ".config", "jedgebot", self.username
            )

        os.makedirs(base_dir, exist_ok=True)  # Ensure directory exists
        return os.path.join(base_dir, "tastytrade_tokens.json")

    def _load_tokens(self):
        """Load session and remember tokens from file."""
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as file:
                data = json.load(file)
                self.session_token = data.get("session_token")
                self.remember_token = data.get("remember_token")
                self.session_expiration = data.get("session_expiration")
                print(
                    f"🔍 Loaded tokens: session_token={self.session_token}, remember_token={self.remember_token}, session_expiration={self.session_expiration}"
                )

    def _save_tokens(self):
        """Save session and remember tokens to file."""
        data = {
            "session_token": self.session_token,
            "remember_token": self.remember_token,
            "session_expiration": self.session_expiration,
        }
        with open(self.token_file, "w") as file:
            json.dump(data, file)
        print(f"✅ Tokens saved to {self.token_file}: {data}")

    def is_session_valid(self):
        """Check if the session token is still valid."""
        if self.session_expiration:
            expiration_time = datetime.datetime.fromisoformat(
                self.session_expiration.replace("Z", "")
            )
            return datetime.datetime.utcnow() < expiration_time
        return False

    def ensure_authenticated(self):
        """Ensure session remains valid, refreshing only if necessary."""
        if self.is_session_valid():
            print("✅ Session token is still valid. No login needed.")
            return  # ✅ Keep session open, no login required.

        print("🔄 Session expired. Logging in with password to get a new session token...")
        self.password_used = True  # ✅ Track that we logged in using a password
        self.login(use_remember_token=False)  # ❌ Skip remember-token, always use password


    def login(self, use_remember_token=False):
        """Logs in and stores session token, preferring remember token if available."""
        url = f"{self.BASE_URL}/sessions"
        payload = {"login": self.username, "remember-me": True}

        if use_remember_token and self.remember_token:
            payload["remember-token"] = self.remember_token
            login_method = "remember-token"
        elif self.password:
            payload["password"] = self.password
            login_method = "password"
        else:
            raise ValueError("Either password or remember-token must be provided")

        print(f"🔐 Attempting login using {login_method}...")
        print(f"📤 Payload: {payload}")  # Debugging: Print the payload

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if "session-token" in response_data.get("data", {}):
            self.session_token = response_data["data"]["session-token"]

            # Always store the new session-token
            new_remember_token = response_data["data"].get("remember-token")
            if new_remember_token:
                self.remember_token = new_remember_token

            self.session_expiration = response_data["data"]["session-expiration"]

            # Save session token correctly
            self._save_tokens()
            print(f"✅ Login successful using {login_method}! Session token stored.")

            return self.session_token
        else:
            raise Exception(f"❌ Login failed: {response_data}")

    def logout(self):
        """Logs out and invalidates the session token."""
        if not self.session_token:
            print("⚠️ No active session to logout.")
            return

        url = f"{self.BASE_URL}/sessions"
        headers = {"Authorization": self.session_token}

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print("✅ Logged out successfully.")
            self.session_token = None
            self.session_expiration = None
            self._save_tokens()
        else:
            print(f"❌ Logout failed: {response.json()}")

    def make_request(self, endpoint, method="GET", payload=None):
        """Make an authenticated API request and handle empty responses."""
        if not self.is_session_valid():
            self.ensure_authenticated()

        url = f"{self.BASE_URL}/{endpoint}"
        headers = {
            "Authorization": self.session_token,
            "User-Agent": "TastyTradeClient/1.0"
        }

        response = requests.request(method, url, json=payload, headers=headers)

        if response.status_code == 401:  # Session expired, re-authenticate
            print("🔄 Session expired, re-authenticating...")
            self.ensure_authenticated()
            headers["Authorization"] = self.session_token
            return self.make_request(endpoint, method, payload)

        # ✅ Handle empty API responses safely
        if not response.text.strip():
            print("⚠️ Warning: API returned an empty response!")
            return {"error": "Empty response from API"}

        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"❌ Error decoding JSON: {e}")
            return {"error": "Invalid JSON response from API"}
