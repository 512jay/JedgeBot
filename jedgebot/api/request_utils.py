import requests
import time
from loguru import logger

def request_with_retry(url, method="GET", data=None, headers=None, retries=3, backoff_factor=2):
    """Make an API request with exponential backoff."""
    headers = headers or {}

    for attempt in range(retries):
        try:
            response = requests.request(method, url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                sleep_time = backoff_factor ** attempt
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                logger.error("Max retries reached. Request failed.")
                raise
