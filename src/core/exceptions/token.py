from fastapi import status
from .base import FastAuthError

class TokenError(FastAuthError):
    """Base exception for all token-related errors"""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "TOKEN_ERROR"

class RefreshTokenNotFoundError(TokenError):
    """Raised when a provided refresh token does not exist in the database"""

    error_code = "REFRESH_TOKEN_NOT_FOUND"

    def __init__(self, message: str = "The provided refresh token is invalid or does not exist.") -> None:
        super().__init__(message)


class RefreshTokenAlreadyRevokedError(TokenError):
    """Raised when a user attempts to use or rotate a token that has already been burned"""

    error_code = "REFRESH_TOKEN_REVOKED"


    def __init__(self, message: str = "This refresh token has already been revoked.") -> None:
        super().__init__(message)


class RefreshTokenExpiredError(TokenError):
    """Raised when a refresh token's lifespan has passed its expires_at timestamp"""

    error_code = "REFRESH_TOKEN_EXPIRED"

    def __init__(self, message: str = "This refresh token has expired. Please log in again.") -> None:
        super().__init__(message)

class TokenReuseError(TokenError):
    """Raised when an expired/revoked refresh token is being reused """

    error_code = "TOKEN_REUSE_DETECTED"

    def __init__(self, message: str = "This refresh token has been already used") -> None:
        super().__init__(message)

class InvalidRefreshToken(TokenError):
    """Raised when an invalid refresh token is used for refresh"""

    error_code = "INVALID_REFRESH_TOEKN"

    def __init__(self, message: str = "This refresh token is invalid") -> None:
        super().__init__(message)

