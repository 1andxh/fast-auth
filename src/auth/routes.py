from fastapi import APIRouter, Depends, Request, status

from src.auth.dependecies import AuthServDep, TokenServDep
from src.core.rate_limit.integration import (
    LOGIN_RATE_LIMIT,
    REFRESH_RATE_LIMIT,
    REGISTER_RATE_LIMIT,
)
from src.auth.models import User
from src.auth.schemas import UserResponse

from .dependecies import get_current_user
from .schemas import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/me", response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[REGISTER_RATE_LIMIT],
)
async def register(payload: RegisterRequest, service: AuthServDep):
    return await service.register(email=payload.email, password=payload.password)


@auth_router.post(
    "/login", response_model=TokenResponse, dependencies=[LOGIN_RATE_LIMIT]
)
async def login(
    payload: LoginRequest,
    request: Request,
    service: AuthServDep,
    token_service: TokenServDep,
):
    user = await service.authenticate(email=payload.email, password=payload.password)
    tokens = await token_service.issue_token_pair(
        user=user, user_agent=request.headers.get("User-Agent")
    )
    return TokenResponse(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@auth_router.post(
    "/refresh", response_model=TokenResponse, dependencies=[REFRESH_RATE_LIMIT]
)
async def refresh(payload: RefreshRequest, service: TokenServDep):
    tokens = await service.refresh_tokens(payload.refresh_token)
    return TokenResponse(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: LogoutRequest, service: TokenServDep):
    await service.logout(payload.refresh_token)
