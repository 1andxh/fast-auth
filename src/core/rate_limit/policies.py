from dataclasses import dataclass

from .keys import ip_key, KeyFunction


@dataclass(frozen=True, slots=True)
class Ratelimit:
    limit: int
    key_func: KeyFunction

    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0


class RateLimitPolicies:
    LOGIN_POLICY = Ratelimit(limit=5, minutes=1, key_func=ip_key)
    REGISTER_POLICY = Ratelimit(limit=3, minutes=1, key_func=ip_key)
    REFRESH_POLICY = Ratelimit(limit=30, minutes=1, key_func=ip_key)
