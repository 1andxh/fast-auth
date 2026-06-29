from dataclasses import dataclass
from collections.abc import Callable, Awaitable

from fastapi import Request
from .keys import ip_key

KeyFunction = Callable[[Request], Awaitable[str]]


@dataclass(frozen=True, slots=True)
class Ratelimit:
    limit: int
    key_func: KeyFunction
    minute: int = 0


class RateLimitPolicies:
    LOGIN = Ratelimit(limit=5, minute=1, key_func=ip_key)
    REGISTER = Ratelimit(limit=3, minute=1, key_func=ip_key)
    REFRESH = Ratelimit(limit=30, minute=1, key_func=ip_key)
