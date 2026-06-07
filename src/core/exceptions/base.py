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