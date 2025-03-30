# /backend/core/rate_limit.py
# Centralized rate limiter with support for test-mode disabling.

from typing import Callable, Protocol, cast
from slowapi import Limiter
from slowapi.util import get_remote_address
from backend.core.settings import settings


class LimiterProtocol(Protocol):
    def limit(self, *args, **kwargs) -> Callable: ...


if settings.TESTING:

    class NoOpLimiter:
        def limit(self, *args, **kwargs):
            def decorator(func):
                return func

            return decorator

    limiter = cast(LimiterProtocol, NoOpLimiter())
else:
    limiter = cast(LimiterProtocol, Limiter(key_func=get_remote_address))
