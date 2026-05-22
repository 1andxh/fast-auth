from datetime import datetime, timedelta, timezone
import uuid
import jwt

from src.core.config import settings

JWT_SECRET = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
