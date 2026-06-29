from fastapi import Depends, Request, Response, HTTPException, status
from fastapicap import Cap, RateLimiter
from src.core.config import settings
from src.core.logging.logger import logger
from .policies import Ratelimit
from src.core.exceptions.rate_limit import RateLimitExceededError

cap = Cap.init_app(settings.REDIS_URL)


def _rate_limit_handler(request: Request, response: Response, retry_after: int):
    logger.warning(
        "rate_limit_exceeeded", path=request.url.path, retry_after=retry_after
    )

    raise HTTPException(
        status_code=RateLimitExceededError.status_code,
        detail={
            "error_code": RateLimitExceededError.error_code,
            "message": f"Too many requests. Try again in {retry_after} seconds",
        },
        headers={"Retry-After": str(retry_after)},
    )


async def limiter_dependency(policy: Ratelimit):
    limiter = RateLimiter(
        limit=policy.limit, key_func=policy.key_func, on_limit=_rate_limit_handler
    )
    return Depends(limiter)
