from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import (
    ProfileVerificationServiceDependency,
    UserContextDependency,
    VerificationReadServiceDependency,
    require_role,
)
from src.api.schemas.profile_verification import VerifySchema
from src.command.commands.profile_verification import ProfileVerification, ProfileVerify
from src.command.commands.users import UserRole
from src.query.dto.base import PageMeta, Paginated
from src.query.dto.profile_verification import (
    GetParticularRecordResponse,
    GetVerifiedParticularResponse,
    VerificationDTO,
    VerificationFiltersWithPagination,
    VerifiedDTO,
    VerifiedFiltersWithPagination,
)

router = APIRouter(
    prefix="/verification",
    tags=["Profile Verification(Admin & Volunteer)"],
    dependencies=[Depends(require_role(UserRole.VOLUNTEER, UserRole.ADMIN))],
)


@router.get("/", status_code=200, response_model=Paginated[VerificationDTO])
async def get_pending_verifications(
    filters: Annotated[VerificationFiltersWithPagination, Query()],
    verification_read_service: VerificationReadServiceDependency,
):
    page_meta = PageMeta(page=filters.page, limit=filters.limit)
    new_filters = VerificationFiltersWithPagination(
        **filters.model_dump(
            exclude_none=True, exclude_unset=True, exclude={"page", "limit"}
        )
    )
    return await verification_read_service.get_pending_verifications(
        new_filters, page_meta
    )


@router.get(
    "/verify/{user_id}", status_code=200, response_model=GetParticularRecordResponse
)
async def verificaiton(
    user_id: UUID,
    verification_read_service: VerificationReadServiceDependency,
):
    return await verification_read_service.get_particular_record(user_id=user_id)


@router.post("/verify/{user_id}", status_code=200, response_model=ProfileVerification)
async def verify(
    cmd: VerifySchema,
    user_context: UserContextDependency,
    profile_verification_service: ProfileVerificationServiceDependency,
):
    return await profile_verification_service.update_status(
        ProfileVerify(
            verified_by=user_context.user_id,
            id=cmd.id,
            status=cmd.status,
            remarks=cmd.remarks,
        )
    )


@router.get("/verified", status_code=200, response_model=Paginated[VerifiedDTO])
async def get_verified_entries(
    filters: Annotated[VerifiedFiltersWithPagination, Query()],
    verification_read_service: VerificationReadServiceDependency,
):
    page_meta = PageMeta(page=filters.page, limit=filters.limit)
    new_filters = VerifiedFiltersWithPagination(
        **filters.model_dump(
            exclude_none=True, exclude_unset=True, exclude={"page", "limit"}
        )
    )
    return await verification_read_service.get_verified_entries(new_filters, page_meta)


# get_verified_particular_record
@router.get(
    "/verified/{user_id}", status_code=200, response_model=GetVerifiedParticularResponse
)
async def verified_record(
    user_id: UUID,
    verification_read_service: VerificationReadServiceDependency,
):
    return await verification_read_service.get_verified_particular_record(
        user_id=user_id
    )
