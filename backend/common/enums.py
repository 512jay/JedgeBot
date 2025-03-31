# /backend/common/enums.py
# Shared enums across the JedgeBot backend.

from enum import Enum  # only import this once


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"

    def __str__(self):
        return self.name  # Returns "MARKET", "LIMIT", etc.


class UserRole(str, Enum):
    trader = "trader"
    client = "client"
    manager = "manager"
    enterprise = "enterprise"


class UserStatus(str, Enum):
    active = "active"
    grace = "grace"
    downgraded = "downgraded"
    banned = "banned"
    deactivated = "deactivated"
