from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import Field

from src.api.dependencies import (
    AcademicDetailsServiceDependency,
    CollegeLookupServiceDependency,
    LocationLookupServiceDependency,
    ParentalDetailsServiceDependency,
    PersonalDetailsServiceDependency,
    ProfileVerificationServiceDependency,
    UserContextDependency,
    VerifyProfileCompletionServiceDependency,
    require_role,
)
from src.api.schemas.profile_completion import (
    AcademicUpdateSchema,
    FileUploadCommand,
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
from src.command.commands.college_lookup import CollegeLookupGet
from src.command.commands.media import MediaStatusEnum, MediaUpdate
from src.command.commands.personal_details import PersonalDetailsCreate
from src.command.commands.profile_verification import (
    ProfileVerificationCreate,
    ProfileVerificationGet,
    ProfileVerificationStatusEnum,
)
from src.command.commands.users import UserRole
from src.command.services.profile_verification import InitializeMedia

profile_completion_router = APIRouter(
    prefix="/profile-completion",
    tags=["Complete Your Profile"],
    dependencies=[Depends(require_role(UserRole.STUDENT))],
    deprecated=True,
)


@profile_completion_router.post("/personal-details")
async def create_personal_details(
    cmd: PersonalDetailsSchema,
    personal_service: PersonalDetailsServiceDependency,
    user_context: UserContextDependency,
):

    return await personal_service.create(
        PersonalDetailsCreate(
            id=user_context.user_id,
            created_by=user_context.user_id,
            **cmd.model_dump(mode="json"),
        )
    )


@profile_completion_router.post("/parental-details")
async def create_parental_details(
    cmd: ParentalDetailsSchema,
    parental_service: ParentalDetailsServiceDependency,
    user_context: UserContextDependency,
):

    return await parental_service.create(cmd.to_create(user_id=user_context.user_id))


@profile_completion_router.get("/academic-details/status")
async def check_academic_status(
    user_context: UserContextDependency,
    academic_service: AcademicDetailsServiceDependency,
):
    await academic_service.check_currently_enrolled(
        AcademicDetailsGetAll(id=user_context.user_id)
    )

    return {"message": "Academic details saved successfully"}


@profile_completion_router.get("/academic-details")
async def get_academic_details(
    user_context: UserContextDependency,
    academic_service: AcademicDetailsServiceDependency,
):
    return await academic_service.get_all(
        AcademicDetailsGetAll(id=user_context.user_id)
    )


@profile_completion_router.post("/academic-details/create")
async def create_academic_detail(
    cmd: AcademicDetails,
    academic_service: AcademicDetailsServiceDependency,
    user_context: UserContextDependency,
):

    return await academic_service.create(
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
    user_context: UserContextDependency,
    academic_service: AcademicDetailsServiceDependency,
):
    return await academic_service.update(
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
    user_context: UserContextDependency,
    academic_service: AcademicDetailsServiceDependency,
):
    await academic_service.delete(
        AcademicDetailsDelete(
            id=user_context.user_id,
            deleted_by=user_context.user_id,
            level_of_education=level_of_education,
        )
    )

    return {"message": "Academic details deleted successfully"}


@profile_completion_router.get("/status")
async def get_completion_status(
    verify_profile_completion_service: VerifyProfileCompletionServiceDependency,
    user_context: UserContextDependency,
):

    result = await verify_profile_completion_service.is_completed(
        id=user_context.user_id
    )

    return ProfileCompletionStatus(
        personal_details=result[0],
        academic_details=result[1],
        parental_details=result[2],
        id_uploaded=result[3],
    )


@profile_completion_router.get(
    "/pincode/{pincode}", response_model=PincodeLookupResponse
)
async def get_location_by_pincode(
    pincode: Annotated[str, Field(pattern=r"^\d{6}$")],
    location_service: LocationLookupServiceDependency,
):
    return await location_service.lookup_pincode(pincode)


@profile_completion_router.get("/college/{college_name}")
async def get_college_by_name(
    college_name: str,
    college_lookup_service: CollegeLookupServiceDependency,
):
    return {
        "colleges": await college_lookup_service.get(
            CollegeLookupGet(name=college_name)
        )
    }


# @profile_completion_router.post("/get-presigned-url")
# async def get_presigned_url(
#     cmd: FileUploadCommand,
#     s3_bucket: S3BucketDependency,
#     user_context: UserContextDependency,
# ):
#     url = await s3_bucket.get_upload_url(
#         metadata=FileMetadata(
#             key="profile-verification/" + str(user_context.user_id) + ".pdf",
#             filename=cmd.filename,
#             content_type=cmd.content_type,
#         )
#     )

#     return {
#         "presigned-url": url,
#         "path": "profile-verification/" + str(user_context.user_id) + ".pdf",
#     }


@profile_completion_router.post("/initialize-upload")
async def initialize_upload(
    cmd: FileUploadCommand,
    profile_verification_service: ProfileVerificationServiceDependency,
    user_context: UserContextDependency,
):
    return await profile_verification_service.initialize(
        InitializeMedia(
            created_by=user_context.user_id,
            filename=cmd.filename,
            file_size=cmd.file_size,
            content_type=cmd.content_type,
        )
    )


@profile_completion_router.post("/upload-success")
async def upload_success(
    media_id: str,
    profile_verification_service: ProfileVerificationServiceDependency,
    user_context: UserContextDependency,
):
    return await profile_verification_service.create(
        ProfileVerificationCreate(
            id=user_context.user_id,
            media_id=UUID(media_id),
            created_by=user_context.user_id,
            status=ProfileVerificationStatusEnum.PENDING,
        )
    )


@profile_completion_router.delete("/upload-failure")
async def file_upload_failure(
    media_id: str,
    profile_verification_service: ProfileVerificationServiceDependency,
    user_context: UserContextDependency,
):
    await profile_verification_service.upload_failure(
        MediaUpdate(
            id=UUID(media_id),
            status=MediaStatusEnum.FAILED,
            updated_by=user_context.user_id,
        )
    )


@profile_completion_router.get("/get-document/{id}")
async def get_profile_completion(
    id: str,
    profile_verification_service: ProfileVerificationServiceDependency,
    user_context: UserContextDependency,
):
    return await profile_verification_service.get_file_url(
        cmd=ProfileVerificationGet(id=UUID(id))
    )
