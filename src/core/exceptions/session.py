from fastapi import status
from .base import FastAuthError

class SessionError(FastAuthError):
    """Base exception for all session-related lifecycle failures."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "SESSION_ERROR"

class SessionNotFoundError(SessionError):
    error_code = "SESSION_NOT_FOUND"

    def __init__(self, message: str = "The requested session does not exist") -> None:
        super().__init__(message)


class SessionRevokedError(SessionError):
    error_code = "SESSION_REVOKED"

    def __init__(self, message: str = "This session has been explicitly revoked") -> None:
        super().__init__(message)


class SessionExpiredError(SessionError):
    error_code = "SESSION_EXPIRED"

    def __init__(self, message: str = "This session has expired due to inactivity") -> None:
        super().__init__(message)