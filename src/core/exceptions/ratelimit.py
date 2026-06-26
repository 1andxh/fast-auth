from fastapi import status
from .base import FastAuthError


class RateLimitExceededError(FastAuthError):
    """Raised whne rate limit is exceeded"""

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    error_code = "RATE_LIMIT_EXCEEDED"

    def __init__(self, message: str = "Too many requests") -> None:
        super().__init__(message)
