from fastapi import status
from .base import FastAuthError


class RateLimitExceededError(FastAuthError):
    """Raised whne rate limit is exceeded"""

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    error_code = "RATE_LIMIT_EXCEEDED"

    def __init__(
        self,
        retry_after: int | None = None,
        message: str = "Too many requests. Please try again later",
    ) -> None:
        super().__init__(message)
        self.retry_after = retry_after
