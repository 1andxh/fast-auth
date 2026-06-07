from fastapi import status
from .base import FastAuthError

class AuthError(FastAuthError):
    """Base authentication exception."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "AUTHENTICATION_FAILED"


class InvalidTokenError(AuthError):
    """Token is malformed, signature is invalid, or parsing failed."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "INVALID_TOKEN"

    def __init__(self, message: str = "Token is invalid or malformed.") -> None:
        super().__init__(message)


class ExpiredTokenError(AuthError):
    """Token expiration timestamp (exp) has passed."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "EXPIRED_TOKEN"

    def __init__(self, message: str = "Token has expired.") -> None:
        super().__init__(message)


class InvalidTokenTypeError(AuthError):
    """Token type is incorrect (e.g., using an access token where a refresh token is expected)."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "INVALID_TOKEN_TYPE"

    def __init__(self, message: str = "Invalid token type provided.") -> None:
        super().__init__(message)


class RefreshTokenReuseError(AuthError):
    """A used/revoked refresh token was submitted (potential breach attempt)."""

    status_code = status.HTTP_403_FORBIDDEN
    error_code = "REFRESH_TOKEN_REUSE_DETECTED"

    def __init__(
        self, message: str = "Refresh token reuse detected! Security breach alert."
    ) -> None:
        super().__init__(message)

class InvalidCredentialsError(AuthError):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "INVALID_AUTHENTICATION_CREDENTIALS"

    def __init__(self, message: str = "Invalid authentication credentials provided") -> None:
        super().__init__(message)

class InactiveUserError(AuthError):
    """Raised when login for an inactive user is detected"""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "INACTIVE_USER"

    def __init__(self, message: str = "User account is currently inactive") -> None:
        super().__init__(message)
