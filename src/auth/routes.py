from fastapi import APIRouter, Depends, status
from src.users.schemas import UserResponse
from src.users.models import User
from .schemas import RegisterRequest, LoginRequest, TokenResponse, TokenPayload
from .dependecies import get_current_user, get_auth_service
from .services import AuthService, TokenService
from typing import Annotated

auth_router = APIRouter(prefix="/auth")
service = Annotated[AuthService, Depends(get_auth_service)]


@auth_router.get("/me", response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, service: service):
    user = await service.register(email=payload.email, password=payload.password)

    return user

@auth_router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, service: service, token_service: TokenService):
    user = await service.authenticate(email=payload.email, password=payload.password)
    tokens = await token_service.issue_token_pair(user=user)