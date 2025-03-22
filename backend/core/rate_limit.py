# /backend/core/rate_limit.py

import os
from typing import Callable, Protocol, cast
from slowapi import Limiter
from slowapi.util import get_remote_address


# Define interface for limiter behavior
class LimiterProtocol(Protocol):
    def limit(self, *args, **kwargs) -> Callable: ...


TESTING = os.getenv("TESTING", "false").lower() == "true"

if TESTING:

    class NoOpLimiter:
        def limit(self, *args, **kwargs):
            def decorator(func):
                return func

            return decorator

    limiter = cast(LimiterProtocol, NoOpLimiter())  # ✅ trusted cast
else:
    limiter = cast(
        LimiterProtocol, Limiter(key_func=get_remote_address)
    )  # ✅ trusted cast
