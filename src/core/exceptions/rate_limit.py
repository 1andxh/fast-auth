from fastapi import status
from .base import FastAuthError


class RateLimitExceededError(FastAuthError):
    """Raised when rate limit is exceeded"""

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    error_code = "RATE_LIMIT_EXCEEDED"

    def __init__(
        self,
        retry_after: int | None = None,
        message: str = "Too many requests. Please try again later",
    ) -> None:
        headers = {"Retry-After": str(retry_after)} if retry_after is not None else None
        super().__init__(message, headers=headers)
        self.retry_after = retry_after
