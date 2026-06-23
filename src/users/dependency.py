from src.db.dependency import DbSession
from .services import UserService


async def get_user_service(session: DbSession) -> UserService:
    return UserService(session)
