from fastapi import status
from .base import FastAuthError

class TokenError(FastAuthError):
    """Base exception for all token-related errors"""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "TOKEN_ERROR"

class RefreshTokenNotFoundError(TokenError):
    """Raised when a provided refresh token does not exist in the database"""

    error_code = "REFRESH_TOKEN_NOT_FOUND"
    message = "The provided refresh token is invalid or does not exist."


class RefreshTokenAlreadyRevokedError(TokenError):
    """Raised when a user attempts to use or rotate a token that has already been burned"""

    error_code = "REFRESH_TOKEN_REVOKED"
    message = "This refresh token has already been revoked."

class RefreshTokenExpiredError(TokenError):
    """Raised when a refresh token's lifespan has passed its expires_at timestamp"""

    error_code = "REFRESH_TOKEN_EXPIRED"
    message = "This refresh token has expired. Please log in again."
