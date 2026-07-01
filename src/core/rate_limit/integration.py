from fastapi import Depends, Request, Response, HTTPException
from fastapicap import Cap, RateLimiter
from src.core.config import settings
from src.core.logging.logger import logger
from .policies import Ratelimit, RateLimitPolicies
from src.core.exceptions.rate_limit import RateLimitExceededError

cap = Cap.init_app(settings.REDIS_URL)


async def _on_rate_limit(
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


def _create_rate_limiter(policy: Ratelimit) -> RateLimiter:
    return RateLimiter(
        limit=policy.limit,
        seconds=policy.seconds,
        minutes=policy.minutes,
        hours=policy.hours,
        days=policy.days,
        key_func=policy.key_func,  # type: ignore
        on_limit=_on_rate_limit,  # type: ignore
    )


def _create_dependency(policy: Ratelimit):
    limiter = _create_rate_limiter(policy)

    return Depends(limiter)
