from typing import Annotated

from fastapi import Cookie, Depends

from src.command.commands.authentication import GetUserByToken, UserContext
from src.command.commands.users import UserRole
from src.command.services.academic_details import AcademicDetailsService
from src.command.services.authentication import AuthenticationService
from src.command.services.college_lookup import CollegeLookupService
from src.command.services.location_lookup import LocationLookupService
from src.command.services.parental_details import ParentalDetailsService
from src.command.services.personal_details import PersonalDetailsService
from src.command.services.profile_verification import ProfileVerificationService
from src.command.services.verify_profile_completion import (
    VerifyProfileCompletionService,
)
from src.core.email.email_service import EmailService
from src.core.storage.s3 import S3Bucket
from src.dependencies import (
    academic_service,
    authentication_service,
    college_lookup_service,
    email_service,
    location_lookup_service,
    parental_service,
    personal_service,
    profile_verification_service,
    s3_bucket,
    verify_profile_completion_service,
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


def get_verify_profile_completion_service() -> VerifyProfileCompletionService:
    return verify_profile_completion_service


VerifyProfileCompletionServiceDependency = Annotated[
    VerifyProfileCompletionService, Depends(get_verify_profile_completion_service)
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


"""
S3 Dependency
"""


def get_s3_bucket() -> S3Bucket:
    return s3_bucket


S3BucketDependency = Annotated[S3Bucket, Depends(get_s3_bucket)]


"""
Email Dependency
"""


def get_email_service() -> EmailService:
    return email_service


EmailServiceDependency = Annotated[EmailService, Depends(get_email_service)]

"""
Personal, Parental and Academic Details Dependency
"""


def get_academic_service() -> AcademicDetailsService:
    return academic_service


AcademicDetailsServiceDependency = Annotated[
    AcademicDetailsService, Depends(get_academic_service)
]


def get_personal_service() -> PersonalDetailsService:
    return personal_service


PersonalDetailsServiceDependency = Annotated[
    PersonalDetailsService, Depends(get_personal_service)
]


def get_parent_service() -> ParentalDetailsService:
    return parental_service


ParentalDetailsServiceDependency = Annotated[
    ParentalDetailsService, Depends(get_parent_service)
]


"""
Profile Verification Dependency
"""


def get_profile_verification_service() -> ProfileVerificationService:
    return profile_verification_service


ProfileVerificationServiceDependency = Annotated[
    ProfileVerificationService, Depends(get_profile_verification_service)
]
