from src.db.dependency import session
from .services import UserService


async def get_user_service(session: session) -> UserService:
    return UserService(session)
