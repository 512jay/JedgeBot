from log_setup import logger

class TastyTradeDataHandler:
    def __init__(self):
        self.data = {}
        logger.info("TastyTradeDataHandler initialized.")

    def update_data(self, key, value):
        """Update stored data with new values."""
        logger.debug(f"Updating data: {key} -> {value}")
        self.data[key] = value

    def get_data(self, key):
        """Retrieve stored data."""
        logger.debug(f"Retrieving data for key: {key}")
        return self.data.get(key, None)

    def clear_data(self):
        """Clear all stored data."""
        logger.warning("Clearing all stored data.")
        self.data.clear()

    def handle_stream_update(self, data):
        """Process incoming stream updates."""
        logger.info(f"Handling stream update: {data}")
        for key, value in data.items():
            self.update_data(key, value)

logger.info("TastyTradeDataHandler setup complete.")
