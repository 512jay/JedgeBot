# jedgebot/common/enums.py
from enum import Enum


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"

    def __str__(self):
        return self.name  # Returns "MARKET", "LIMIT", etc.
