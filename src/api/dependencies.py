from typing import Annotated

from fastapi import Cookie, Depends

from src.command.commands.authentication import GetUserByToken, UserContext
from src.command.commands.users import UserRole
from src.command.services.authentication import AuthenticationService
from src.command.services.college_lookup import CollegeLookupService
from src.command.services.location_lookup import LocationLookupService
from src.command.services.profile_completion import ProfileCompletionService
from src.dependencies import (
    authentication_service,
    college_lookup_service,
    location_lookup_service,
    profile_completion_service,
)
from src.exceptions import UnAuthenticatedError, UnAuthorizedError

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


def require_role(*allowed_roles: UserRole):
    async def role_checker(
        user_context: UserContextDependency,
    ) -> UserContext:
        if user_context.role not in allowed_roles:
            raise UnAuthorizedError(
                message="You do not have permission to access this resource",
            )
        return user_context

    return role_checker


type UserContextDependency = Annotated[UserContext, Depends(get_current_user_context)]


"""
2. Authentication Dependency
"""


def get_authentication_service() -> AuthenticationService:
    return authentication_service


AuthenticationServiceDependency = Annotated[
    AuthenticationService, Depends(get_authentication_service)
]


"""
3. Complete your Profile Dependency
"""


def get_profile_completion_service() -> ProfileCompletionService:
    return profile_completion_service


ProfileCompletionServiceDependency = Annotated[
    ProfileCompletionService, Depends(get_profile_completion_service)
]


"""
4. Location Lookup Dependency
"""


def get_location_lookup_service() -> LocationLookupService:
    return location_lookup_service


LocationLookupServiceDependency = Annotated[
    LocationLookupService, Depends(get_location_lookup_service)
]


"""
5. College Lookup Dependency
"""


def get_college_lookup_service() -> CollegeLookupService:
    return college_lookup_service


CollegeLookupServiceDependency = Annotated[
    CollegeLookupService, Depends(get_college_lookup_service)
]
