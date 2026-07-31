from typing import Annotated

from fastapi import Cookie, Depends

from src.command.commands.authentication import GetUserByToken, UserContext
from src.command.services.authentication import AuthenticationService
from src.dependencies import authentication_service
from src.exceptions import UnAuthenticatedError

"""
1. User Context Dependency
"""


async def get_current_user_context(
    access_token: Annotated[str | None, Cookie()] = None,
) -> UserContext:
    if access_token is None:
        raise UnAuthenticatedError(message="No access token provided.")

    user_context = await authentication_service.me(
        token=GetUserByToken(token=access_token)
    )

    return user_context


type UserContextDependency = Annotated[UserContext, Depends(get_current_user_context)]


"""
2. Authentication Dependency
"""


def get_authentication_service() -> AuthenticationService:
    return authentication_service


AuthenticationServiceDependency = Annotated[
    AuthenticationService, Depends(get_authentication_service)
]
