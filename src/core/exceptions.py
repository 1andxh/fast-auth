class AuthError(Exception):
    """Base authentication exception."""


class InvalidTokenError(AuthError):
    """Token is malformed or invalid."""


class ExpiredTokenError(AuthError):
    """Token has expired."""


class InvalidTokenTypeError(AuthError):
    """Token type is invalid."""


class RefreshTokenReuseError(AuthError):
    """Refresh token reuse detected."""
