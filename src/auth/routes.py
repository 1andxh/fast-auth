from fastapi import APIRouter, Depends, status, Request
from src.users.schemas import UserResponse
from src.users.models import User
from .schemas import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest, LogoutRequest
from .dependecies import get_current_user
from src.auth.dependecies import AuthServDep, TokenServDep

auth_router = APIRouter(prefix="/auth")

@auth_router.get("/me", response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, service: AuthServDep):
    return await service.register(email=payload.email, password=payload.password)


@auth_router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request, service: AuthServDep, token_service: TokenServDep):
    user = await service.authenticate(email=payload.email, password=payload.password)
    tokens = await token_service.issue_token_pair(user=user, user_agent=request.headers.get("User-Agent"))
    return TokenResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, service: TokenServDep):
    tokens = await service.refresh_tokens(payload.refresh_token)
    return TokenResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)
    

@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: LogoutRequest, service: TokenServDep):
    await service.logout(payload.refresh_token)
