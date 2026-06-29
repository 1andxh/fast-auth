from dataclasses import dataclass
from collections.abc import Callable, Awaitable

from fastapi import Request
from .keys import ip_key

KeyFunction = Callable[[Request], Awaitable[str]]


@dataclass(frozen=True, slots=True)
class Ratelimit:
    limit: str
    key_func: KeyFunction


class RateLimitPolicies:
    LOGIN = Ratelimit(limit="5/minute", key_func=ip_key)
    REGISTER = Ratelimit(limit="3/minute", key_func=ip_key)
    REFRESH = Ratelimit(limit="30/minute", key_func=ip_key)
