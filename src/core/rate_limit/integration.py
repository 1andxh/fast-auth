from fastapi import Depends, Request, Response, HTTPException
from fastapicap import Cap, RateLimiter
from src.core.config import settings
from src.core.logging.logger import logger
from .policies import Ratelimit
from src.core.exceptions.rate_limit import RateLimitExceededError

cap = Cap.init_app(settings.REDIS_URL)


async def _rate_limit_handler(
    request: Request, response: Response, retry_after: int
) -> None:
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


def limiter_dependency(policy: Ratelimit):
    limiter = RateLimiter(
        limit=policy.limit,
        minutes=policy.minutes,
        key_func=policy.key_func,  # type: ignore
        on_limit=_rate_limit_handler,  # type: ignore[arg-type] | ignored due to library's current annotation
    )
    return Depends(limiter)
