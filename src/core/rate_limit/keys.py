from fastapi import Request


async def ip_key(request: Request) -> str:

    forwarded = request.headers.get("X-Forwarded-FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()

    if request.client is None:
        return "Unknown"

    return request.client.host


async def session_key(): ...


async def user_key(): ...
