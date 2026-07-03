from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.logging.logger import configure_logging

configure_logging()

from fastapicap import Cap  # noqa: E402

from src.api.router import router  # noqa: E402
from src.core.config import settings  # noqa: E402
from src.core.exception_handlers import (  # noqa: E402
    FastAuthError,
    RequestValidationError,
    fast_auth_exception_handler,
    general_exception_handler,
    request_validation_handler,
)
from src.core.middleware import RequestIDMiddleware  # noqa: E402

version = settings.VERSION


@asynccontextmanager
async def lifespan(app: FastAPI):
    Cap.init_app(settings.REDIS_URL)
    yield


app = FastAPI(title=settings.APP_NAME, version=version, lifespan=lifespan)


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
