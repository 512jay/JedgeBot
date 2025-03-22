import requests

BASE_URL = "http://localhost:8000"


def test_rate_limit(endpoint, attempts=6):
    print(f"\n🔁 Testing {endpoint} ({attempts} attempts)")
    for i in range(attempts):
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            json=(
                {"email": "user@example.com", "password": "wrongpass"}
                if "login" in endpoint
                else {"email": "user@example.com"}
            ),
        )
        print(f"Attempt {i+1}: {response.status_code} {response.reason}")
        if response.status_code == 429:
            print("🚫 Rate limit enforced as expected.")
            break


test_rate_limit("/auth/login")
test_rate_limit("/forgot-password")
