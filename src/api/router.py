from fastapi import APIRouter
from src.auth.routes import auth_router

router = APIRouter()


# all other routers
router.include_router(auth_router)
