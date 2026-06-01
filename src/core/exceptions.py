class FastAuthError(Exception):
    """Base exception for FastAuth"""

    status_code: int
    message: str


# identity exception
class UserError(FastAuthError):
    """Base identity exception"""


class DuplicateEmailError(UserError):
    """Email already exists"""


class UserNotFoundError(UserError):
    """User does not exists or not found"""


class UserAlreadyVerified(UserError):
    """User already verified identity"""


# auth exceptions
class AuthError(FastAuthError):
    """Base authentication exception."""


class InvalidTokenError(AuthError):
    """Token is malformed or invalid."""


class ExpiredTokenError(AuthError):
    """Token has expired."""


class InvalidTokenTypeError(AuthError):
    """Token type is invalid."""


class RefreshTokenReuseError(AuthError):
    """Refresh token reuse detected."""
