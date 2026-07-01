from fastapi import Request
from collections.abc import Callable, Awaitable

KeyFunction = Callable[[Request], Awaitable[str]]


async def ip_key(request: Request) -> str:
    """
    Returns the client identity used for IP-based rate limiting.

    """
    client = request.client
    forwarded_client = request.headers.get("X-Forwarded-FOR")
    if forwarded_client:
        return forwarded_client.split(",")[0].strip()

    if client is None:
        raise RuntimeError("Request client address is unavailable")

    return client.host


async def session_key(): ...


async def user_key(): ...
