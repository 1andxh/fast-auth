import uuid
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from .logging.context import request_id_ctx
from structlog.contextvars import bind_contextvars, clear_contextvars


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid.uuid4())
        request_id_ctx.set(request_id)
        bind_contextvars(request_id=request_id)

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        response.headers["X-Process-time"] = str(duration)
        response.headers["X-Request-ID"] = request_id

        clear_contextvars()
        return response
