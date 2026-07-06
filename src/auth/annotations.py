from typing import Annotated

from fastapi import Depends

from src.auth import Security, get_security

SecurityDep = Annotated[Security, Depends(get_security)]
