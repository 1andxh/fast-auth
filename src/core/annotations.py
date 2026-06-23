from __future__ import annotations
from fastapi import Depends
from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from src.users.services import UserService
    from src.auth import Security, get_security, RefreshTokenService, TokenService, SessionService, AuthService, get_session_service, get_auth_service, get_refresh_service, get_token_service
    from src.users.dependency import get_user_service


UserServDep = Annotated[UserService, Depends(get_user_service)]
SecurityDep = Annotated[Security, Depends(get_security)]
AuthServDep = Annotated[AuthService, Depends(get_auth_service)]
RefreshServDep = Annotated[RefreshTokenService, Depends(get_refresh_service)]
SessionServDep = Annotated[SessionService, Depends(get_session_service)]
TokenServDep = Annotated[TokenService, Depends(get_token_service)]
