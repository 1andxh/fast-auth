from fastapi import status


class FastAuthError(Exception):
    """Base exception for all FastAuth errors."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "INTERNAL_ERROR"

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        error_code: str | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code
        super().__init__(message)


class UserError(FastAuthError):
    """Base identity exception."""

    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "USER_ERROR"


class DuplicateEmailError(UserError):
    """Email already exists in the system."""

    status_code = status.HTTP_409_CONFLICT
    error_code = "DUPLICATE_EMAIL"

    def __init__(self, message: str = "Email already exists.") -> None:
        super().__init__(message)


class UserNotFoundError(UserError):
    """User does not exist or could not be found."""

    status_code = status.HTTP_404_NOT_FOUND
    error_code = "USER_NOT_FOUND"

    def __init__(self, message: str = "User not found.") -> None:
        super().__init__(message)


class UserAlreadyVerified(UserError):
    """User has already verified their identity/email."""

    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "USER_ALREADY_VERIFIED"

    def __init__(self, message: str = "User identity is already verified.") -> None:
        super().__init__(message)


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
