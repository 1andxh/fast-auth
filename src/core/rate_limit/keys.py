from fastapi import Request


async def ip_key(request: Request) -> str:
    """
    Returns the client identity used for IP-based rate limiting.

    Supports reverse proxies by preferring X-Forwarded-For.
    Falls back to the client socket address.
    """

    forwarded = request.headers.get("X-Forwarded-FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()

    if request.client is None:
        return "unknown"

    return request.client.host


async def session_key(): ...


async def user_key(): ...
