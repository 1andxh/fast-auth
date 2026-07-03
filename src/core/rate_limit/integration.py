from fastapi import Depends, Request, Response
from fastapi.params import Depends as DependsType
from fastapicap import RateLimiter

from src.core.exceptions.rate_limit import RateLimitExceededError
from src.core.logging.logger import logger
from src.core.rate_limit.policies import (
    LOGIN_POLICY,
    REFRESH_POLICY,
    REGISTER_POLICY,
    Ratelimit,
)


async def _on_rate_limit(
    request: Request, response: Response, retry_after: int
) -> None:
    logger.warning(
        "rate_limit_exceeded",
        path=request.url.path,
        method=request.method,
        retry_after=retry_after,
        client=request.client.host if request.client else None,
    )

    raise RateLimitExceededError(retry_after=retry_after)


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


def _create_dependency(policy: Ratelimit) -> DependsType:
    limiter = _create_rate_limiter(policy)

    return Depends(limiter)


LOGIN_RATE_LIMIT = _create_dependency(LOGIN_POLICY)
REGISTER_RATE_LIMIT = _create_dependency(REGISTER_POLICY)
REFRESH_RATE_LIMIT = _create_dependency(REFRESH_POLICY)
