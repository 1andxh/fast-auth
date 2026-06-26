from fastapi import FastAPI

from src.core.logging.logger import configure_logging

configure_logging()  # should run before any module that calls logger instance at import

from src.core.config import settings
from src.api.router import router
from src.core.middleware import RequestIDMiddleware
from src.core.exception_handlers import (
    FastAuthError,
    fast_auth_exception_handler,
    general_exception_handler,
    RequestValidationError,
    request_validation_handler,
)

version = settings.VERSION


app = FastAPI(title=settings.APP_NAME, version=version)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router, prefix="/api/v1")

# middleware
app.add_middleware(RequestIDMiddleware)

# exceptions
app.add_exception_handler(FastAuthError, fast_auth_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)  # type: ignore
app.add_exception_handler(Exception, general_exception_handler)
