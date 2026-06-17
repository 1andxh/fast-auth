from fastapi import APIRouter, Depends
from src.users.schemas import UserResponse
from src.users.models import User
from .dependecies import get_current_user

auth_router = APIRouter()

@auth_router.get("/me", response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user