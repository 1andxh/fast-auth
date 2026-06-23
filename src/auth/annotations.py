from fastapi import Depends
from typing import Annotated

from src.auth import Security, get_security
from src.users import UserService, get_user_service


UserServDep = Annotated[UserService, Depends(get_user_service)]
SecurityDep = Annotated[Security, Depends(get_security)]
