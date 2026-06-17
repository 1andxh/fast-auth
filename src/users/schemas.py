from pydantic import BaseModel
import uuid
from datetime import datetime

class UserResponse(BaseModel):
    id: uuid.UUID 
    email: str
    is_active: bool
    is_verified: bool
    created_at: datetime