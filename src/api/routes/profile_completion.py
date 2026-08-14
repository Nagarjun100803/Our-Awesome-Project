from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import Field

from src.api.dependencies import (
    LocationLookupServiceDependency,
    ProfileCompletionServiceDependency,
    UserContextDependency,
    require_role,
)
from src.api.schemas.profile_completion import (
    AcademicUpdateSchema,
    ParentalDetailsSchema,
    PersonalDetailsSchema,
    PincodeLookupResponse,
    ProfileCompletionStatus,
)
from src.command.commands.academic_details import (
    AcademicDetails,
    AcademicDetailsCreate,
    AcademicDetailsDelete,
    AcademicDetailsGetAll,
    AcademicDetailsUpadate,
    LevelOfEducationEnum,
)
from src.command.commands.personal_details import PersonalDetailsCreate
from src.command.commands.users import UserRole

profile_completion_router = APIRouter(
    prefix="/profile-completion",
    tags=["Complete Your Profile"],
    dependencies=[Depends(require_role(UserRole.STUDENT))],
)


@profile_completion_router.post("/personal-details")
async def create_personal_details(
    cmd: PersonalDetailsSchema,
    profile_completion_service: ProfileCompletionServiceDependency,
    user_context: UserContextDependency,
):

    return await profile_completion_service.save_personal(
        PersonalDetailsCreate(
            id=user_context.user_id,
            created_by=user_context.user_id,
            **cmd.model_dump(mode="json"),
        )
    )


@profile_completion_router.post("/parental-details")
async def create_parental_details(
    cmd: ParentalDetailsSchema,
    profile_completion_service: ProfileCompletionServiceDependency,
    user_context: UserContextDependency,
):

    return await profile_completion_service.save_parental(
        cmd.to_create(user_id=user_context.user_id)
    )


@profile_completion_router.get("/academic-details/status")
async def check_academic_status(
    profile_completion_service: ProfileCompletionServiceDependency,
    user_context: UserContextDependency,
):
    await profile_completion_service.academic_next(id=user_context.user_id)

    return {"message": "Academic details saved successfully"}


@profile_completion_router.get("/academic-details")
async def get_academic_details(
    profile_completion_service: ProfileCompletionServiceDependency,
    user_context: UserContextDependency,
):
    return await profile_completion_service.get_academic(
        AcademicDetailsGetAll(id=user_context.user_id)
    )


@profile_completion_router.post("/academic-details/create")
async def create_academic_detail(
    cmd: AcademicDetails,
    profile_completion_service: ProfileCompletionServiceDependency,
    user_context: UserContextDependency,
):

    return await profile_completion_service.save_academic(
        AcademicDetailsCreate(
            id=user_context.user_id,
            created_by=user_context.user_id,
            **cmd.model_dump(mode="json"),
        )
    )


@profile_completion_router.patch("/academic-details/update/{level_of_education}")
async def update_academic_details(
    cmd: AcademicUpdateSchema,
    level_of_education: LevelOfEducationEnum,
    profile_completion_service: ProfileCompletionServiceDependency,
    user_context: UserContextDependency,
):
    return await profile_completion_service.update_academic(
        AcademicDetailsUpadate(
            id=user_context.user_id,
            updated_by=user_context.user_id,
            level_of_education=level_of_education,
            **cmd.model_dump(mode="json", exclude_unset=True, exclude_none=True),
        )
    )


@profile_completion_router.delete("/academic-details/delete/{level_of_education}")
async def delete_academic_details(
    level_of_education: LevelOfEducationEnum,
    profile_completion_service: ProfileCompletionServiceDependency,
    user_context: UserContextDependency,
):
    await profile_completion_service.delete_academic(
        AcademicDetailsDelete(
            id=user_context.user_id,
            deleted_by=user_context.user_id,
            level_of_education=level_of_education,
        )
    )
    return {"message": "Academic details deleted successfully"}


@profile_completion_router.get("/status")
async def get_completion_status(
    profile_completion_service: ProfileCompletionServiceDependency,
    user_context: UserContextDependency,
):
    result = await profile_completion_service.is_completed(id=user_context.user_id)

    return ProfileCompletionStatus(
        personal_details=result[0],
        academic_details=result[1],
        parental_details=result[2],
    )


@profile_completion_router.get(
    "/pincode/{pincode}", response_model=PincodeLookupResponse
)
async def get_location_by_pincode(
    pincode: Annotated[str, Field(pattern=r"^\d{6}$")],
    location_service: LocationLookupServiceDependency,
):
    return await location_service.lookup_pincode(pincode)
