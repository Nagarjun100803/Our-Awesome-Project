from typing import Annotated

from fastapi import APIRouter, Query

from src.api.dependencies import (
    UserReadServiceDependency,
    VerificationReadServiceDependency,
)
from src.query.dto.base import PageMeta
from src.query.dto.profile_verification import (
    VerificationFiltersWithPagination,
    VerifiedFiltersWithPagination,
)
from src.query.dto.users import UserFilters, UserFiltersWithPagination

router = APIRouter(prefix="/admin")


@router.get("/users")
async def get(
    filters: Annotated[UserFiltersWithPagination, Query()],
    user_read_service: UserReadServiceDependency,
):
    page_meta = PageMeta(page=filters.page, limit=filters.limit)
    new_filters = UserFilters(
        **filters.model_dump(
            exclude_none=True, exclude_unset=True, exclude={"page", "limit"}
        )
    )
    return await user_read_service.list_users(page_meta, new_filters)


@router.get("/volunteers")
async def get_volunteers(
    user_read_service: UserReadServiceDependency,
):
    return await user_read_service.list_volunteers()


@router.get("/pending-verifications")
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


@router.get("/verified-entries")
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
