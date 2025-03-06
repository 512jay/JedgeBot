import os
import json
import datetime
import requests
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class TastyTradeAuthenticator:
    BASE_URL = "https://api.tastytrade.com"
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session_token = None
        self.token_file = self._get_token_file_path()
        self._load_session_token()

    def _get_token_file_path(self):
        """Returns the path to the session token JSON file in APPDATA."""
        appdata_path = os.getenv("APPDATA") or os.path.expanduser("~/.config/jedgebot")
        os.makedirs(appdata_path, exist_ok=True)
        return os.path.join(appdata_path, "tastytrade_tokens.json")

    def _load_session_token(self):
        """Loads session token from file if available and not expired."""
        logger.info(f"🔍 Looking for session token at: {self.token_file}")

        if not os.path.exists(self.token_file):
            logger.warning("⚠️ Token file not found. Authentication required.")
            return

        with open(self.token_file, "r") as file:
            tokens = json.load(file)

        user_data = tokens.get(self.username, {})
        if not user_data:
            logger.warning(f"⚠️ No token found for {self.username}. Logging in...")
            self.login()
            return

        self.session_token = user_data.get("session-token")
        session_expiration = user_data.get("session-expiration")

        if self.session_token and session_expiration:
            # Convert expiration string to datetime (Tastytrade gives us an ISO timestamp)
            expiration_time = datetime.datetime.fromisoformat(session_expiration.rstrip("Z"))

            # Get current UTC time as a comparable aware datetime object
            current_time = datetime.datetime.utcnow()

            if expiration_time > current_time:
                logger.info(f"🔑 Loaded valid session token (expires: {session_expiration}).")
            else:
                logger.warning(f"⏳ Session expired for {self.username}. Re-authenticating...")
                self.login()
        else:
            logger.warning("⚠️ Invalid token data. Re-authenticating...")
            self.login()

    def _save_session_token(self, token_data):
        """Saves session token details (including expiration) to the JSON file."""
        session_token = token_data.get("session-token")
        remember_token = token_data.get("remember-token")
        session_expiration = token_data.get("session-expiration")

        if not session_token or not session_expiration:
            logger.error("⚠️ Missing session token or expiration. Cannot store session.")
            return

        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as file:
                tokens = json.load(file)
        else:
            tokens = {}

        tokens[self.username] = {
            "session-token": session_token,
            "remember-token": remember_token,
            "session-expiration": session_expiration,
            "email": token_data["user"]["email"],
            "external-id": token_data["user"]["external-id"],
        }

        with open(self.token_file, "w") as file:
            json.dump(tokens, file, indent=4)

        logger.info(f"✅ Stored session token for {self.username} (expires: {session_expiration}).")

    def login(self):
        """Logs in and stores session token details."""
        url = f"{self.BASE_URL}/sessions"
        payload = {"login": self.username, "password": self.password, "remember-me": True}
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        session_data = response_data.get("data", {})
        if "session-token" in session_data:
            self.session_token = session_data["session-token"]
            self._save_session_token(session_data)
            logger.info(f"✅ Login successful for {self.username}. Token expires at {session_data['session-expiration']}.")
        else:
            logger.error(f"❌ Login failed: {response_data}")
            raise Exception("Authentication failed. Check credentials.")

    def get_session_token(self):
        """Returns the current session token, logging in if necessary."""
        if not self.session_token:
            logger.info("🔄 No session token found. Logging in...")
            self.login()
        return self.session_token

    def logout(self):
        """Logs out and removes session token."""
        if not self.session_token:
            logger.warning("No session token found. Already logged out.")
            return

        url = f"{self.BASE_URL}/sessions"
        headers = {"Authorization": self.session_token}

        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            self.session_token = None
            self._clear_session_token()
            logger.info("✅ Logged out successfully.")
        else:
            logger.warning(f"⚠️ Logout request failed: {response.text}")

    def _clear_session_token(self):
        """Removes the stored session token for the current user."""
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as file:
                tokens = json.load(file)

            if self.username in tokens:
                del tokens[self.username]

                with open(self.token_file, "w") as file:
                    json.dump(tokens, file, indent=4)

            logger.info(f"🗑️ Cleared session token for {self.username}.")
