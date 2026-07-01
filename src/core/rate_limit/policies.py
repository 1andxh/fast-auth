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

    def __post_init__(self) -> None:
        if self.limit <= 0:
            raise ValueError("limit must be greater than zero")

        windows = (self.seconds, self.minutes, self.hours, self.days)
        if any(value < 0 for value in windows):
            raise ValueError("time values cannot be negative")
        if sum(windows) == 0:
            raise ValueError("at least one time unit must be provided")


LOGIN_POLICY = Ratelimit(limit=5, minutes=1, key_func=ip_key)
REGISTER_POLICY = Ratelimit(limit=3, minutes=1, key_func=ip_key)
REFRESH_POLICY = Ratelimit(limit=30, minutes=1, key_func=ip_key)
