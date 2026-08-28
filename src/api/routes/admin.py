from typing import Annotated

from fastapi import APIRouter, Query

from src.api.dependencies import (
    UserReadServiceDependency,
)
from src.query.dto.base import PageMeta, Paginated
from src.query.dto.users import UserDTO, UserFilters, UserFiltersWithPagination

router = APIRouter(prefix="/admin", dependencies=[])


@router.get("/users", response_model=Paginated[UserDTO])
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
