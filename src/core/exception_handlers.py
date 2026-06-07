from fastapi.responses import JSONResponse
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError


from .exceptions.base import FastAuthError


async def fast_auth_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, FastAuthError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
            },
        )

    return await general_exception_handler(request, exc)


async def request_validation_handler(request: Request, exc: RequestValidationError):
    formatted_errors = [
        {
            "field": " -> ".join(str(loc) for loc in error.get("loc", [])),
            "type": error.get("type"),
            "message": error.get("msg"),
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "error": "VALIDATION_ERROR",
            "message": "The request payload contains invalid or missing data.",
            "details": formatted_errors,
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    # log traceback for audit
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred on our end. Please try again later.",
        },
    )
