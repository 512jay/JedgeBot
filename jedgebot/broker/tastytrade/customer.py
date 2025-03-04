import json
import os

class Customer:
    def __init__(self, auth):
        """Initialize with an Authentication instance."""
        self.auth = auth  # ✅ Authentication instance, which contains make_request()

    def get_customer_info(self):
        """Fetch basic customer information using Authentication's make_request()."""
        endpoint = "customers/me"
        return self.auth.make_request(endpoint)  # ✅ Now using make_request()

    def save_customer_data(self, filename="customer_data.json"):
        """Fetch customer data and save it as a JSON file in the script directory."""
        data = self.get_customer_info()
        
        if data:
            file_path = os.path.join(os.getcwd(), filename)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            print(f"✅ Customer data saved to {file_path}")
        else:
            print("❌ Failed to retrieve customer data.")

    def get_customer_accounts(self):
        """Fetch the list of accounts associated with the customer."""
        endpoint = "customers/me/accounts"
        return self.auth.make_request(endpoint)  # ✅ Fetch account list

    def save_customer_accounts(self, filename="customer_accounts.json"):
        """Fetch customer accounts and save them as a JSON file in the script directory."""
        accounts = self.get_customer_accounts()
        
        if accounts:
            file_path = os.path.join(os.getcwd(), filename)
            with open(file_path, "w") as f:
                json.dump(accounts, f, indent=4)
            print(f"✅ Customer accounts saved to {file_path}")
        else:
            print("❌ Failed to retrieve customer accounts.")

    def extract_account_numbers(self):
        """Extract and return a list of account numbers from the API response."""
        accounts_response = self.get_customer_accounts()

        if not accounts_response or "data" not in accounts_response:
            print("⚠️ No account data found in response.")
            return []

        account_numbers = []
        items = accounts_response["data"].get("items", [])

        for item in items:
            account_info = item.get("account", {})
            if "account-number" in account_info:
                account_numbers.append(account_info["account-number"])

        if not account_numbers:
            print("⚠️ No accounts found!")
        
        return account_numbers
