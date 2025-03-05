import requests
import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class Authentication:
    BASE_URL = "https://api.tastytrade.com"
    TOKEN_FILE = "session_token.txt"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session_token = None
        self._load_session_token()

    def login(self):
        """Logs in and stores session token."""
        url = f"{self.BASE_URL}/sessions"
        payload = {"login": self.username, "password": self.password, "remember-me": True}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        
        if "session-token" in response_data.get("data", {}):
            self.session_token = response_data["data"]["session-token"]
            self._save_session_token()
            logger.info("✅ Login successful! Session token stored.")
            return self.session_token
        else:
            logger.error(f"❌ Login failed: {response_data}")
            raise Exception("Authentication failed. Check credentials.")

    def logout(self):
        """Logs out and clears session token."""
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

    def get_session_token(self):
        """Returns the current session token, logging in if necessary."""
        if not self.session_token:
            logger.info("🔄 No session token found. Logging in...")
            self.login()
        return self.session_token
    
    def _load_session_token(self):
        """Loads the session token from a file if available."""
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, "r") as file:
                self.session_token = file.read().strip()
                logger.info("🔑 Loaded session token from file.")
    
    def _save_session_token(self):
        """Saves the session token to a file for reuse."""
        with open(self.TOKEN_FILE, "w") as file:
            file.write(self.session_token)
    
    def _clear_session_token(self):
        """Removes the stored session token file."""
        if os.path.exists(self.TOKEN_FILE):
            os.remove(self.TOKEN_FILE)
            logger.info("🗑️ Cleared session token.")

    def ensure_authenticated(self):
        """Ensures authentication is valid or re-authenticates if necessary."""
        if not self.session_token:
            self.login()
