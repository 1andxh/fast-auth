from dataclasses import dataclass
from collections.abc import Callable, Awaitable

from fastapi import Request
from .keys import ip_key

KeyFunction = Callable[[Request], Awaitable[str]]


@dataclass(frozen=True, slots=True)
class Ratelimit:
    limit: int
    key_func: KeyFunction

    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0


class RateLimitPolicies:
    LOGIN = Ratelimit(limit=5, minutes=1, key_func=ip_key)
    REGISTER = Ratelimit(limit=3, minutes=1, key_func=ip_key)
    REFRESH = Ratelimit(limit=30, minutes=1, key_func=ip_key)
