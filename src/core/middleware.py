import uuid
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from .logging.context import request_id_ctx
from structlog.contextvars import bind_contextvars, clear_contextvars
from .logging.logger import logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid.uuid4())
        request_id_ctx.set(request_id)
        bind_contextvars(request_id=request_id)

        start = time.perf_counter()

        logger.info("request_started", method=request.method, path=request.url.path)
        response = await call_next(request)

        duration = time.perf_counter() - start
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            duration=duration,
            status_code=response.status_code,
        )

        response.headers["X-Process-time"] = f"{duration:.4f}"
        response.headers["X-Request-ID"] = request_id

        clear_contextvars()
        return response
