from collections.abc import Awaitable, Callable

from fastapi import Request

from src.core.logging.logger import logger

KeyFunction = Callable[[Request], Awaitable[str]]


async def ip_key(request: Request) -> str:
    """
    Returns the client identity used for IP-based rate limiting.

    """
    client = request.client
    logger.info(
        "rate_limit_key",
        key=request.client.host if request.client is not None else None,
    )

    forwarded_client = request.headers.get("X-Forwarded-FOR")
    if forwarded_client:
        return forwarded_client.split(",")[0].strip()

    if client is None:
        raise RuntimeError("Request client address is unavailable")

    return client.host


async def session_key(): ...


async def user_key(): ...
