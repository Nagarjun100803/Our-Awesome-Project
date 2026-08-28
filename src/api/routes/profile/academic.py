from fastapi import APIRouter

from src.api.dependencies import AcademicDetailsServiceDependency, UserContextDependency
from src.api.schemas.profile_completion import (
    AcademicCreateSchema,
    AcademicUpdateSchema,
)
from src.command.commands.academic_details import (
    AcademicDetails,
    AcademicDetailsCreate,
    AcademicDetailsDelete,
    AcademicDetailsGetAll,
    AcademicDetailsUpadate,
    LevelOfEducationEnum,
)

router = APIRouter(prefix="/academic", tags=["academic details"])


@router.get("/status", status_code=200)
async def check_academic_status(
    user_context: UserContextDependency,
    academic_service: AcademicDetailsServiceDependency,
):
    _ = await academic_service.check_currently_enrolled(
        AcademicDetailsGetAll(id=user_context.user_id)
    )


@router.get("/", status_code=200, response_model=list[AcademicDetails])
async def get_academic_details(
    user_context: UserContextDependency,
    academic_service: AcademicDetailsServiceDependency,
):
    return await academic_service.get_all(
        AcademicDetailsGetAll(id=user_context.user_id)
    )


@router.post("/", status_code=201, response_model=AcademicDetails)
async def create_academic_detail(
    cmd: AcademicCreateSchema,
    academic_service: AcademicDetailsServiceDependency,
    user_context: UserContextDependency,
):

    return await academic_service.create(
        AcademicDetailsCreate(
            id=user_context.user_id,
            created_by=user_context.user_id,
            **cmd.model_dump(mode="json"),  # pyright: ignore[reportAny]
        )
    )


@router.patch("/{level_of_education}", status_code=200, response_model=AcademicDetails)
async def update_academic_details(
    cmd: AcademicUpdateSchema,
    level_of_education: LevelOfEducationEnum,
    user_context: UserContextDependency,
    academic_service: AcademicDetailsServiceDependency,
):
    return await academic_service.update(
        AcademicDetailsUpadate(
            id=user_context.user_id,
            updated_by=user_context.user_id,
            level_of_education=level_of_education,
            **cmd.model_dump(mode="json", exclude_unset=True, exclude_none=True),  # pyright: ignore[reportAny]
        )
    )


@router.delete("/{level_of_education}", status_code=204)
async def delete_academic_details(
    level_of_education: LevelOfEducationEnum,
    user_context: UserContextDependency,
    academic_service: AcademicDetailsServiceDependency,
):
    _ = await academic_service.delete(
        AcademicDetailsDelete(
            id=user_context.user_id,
            deleted_by=user_context.user_id,
            level_of_education=level_of_education,
        )
    )
