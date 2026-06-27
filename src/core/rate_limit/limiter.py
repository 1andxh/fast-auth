from fastapicap import Cap
from src.core.config import settings

cap = Cap.init_app(settings.REDIS_URL)
