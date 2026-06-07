from fastapi import status
from .base import FastAuthError

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