from uuid import UUID

from fastapi import APIRouter

from src.api.dependencies import (
    ProfileVerificationServiceDependency,
    UserContextDependency,
)
from src.api.schemas.profile_completion import FileUploadCommand
from src.command.commands.media import MediaStatusEnum, MediaUpdate
from src.command.commands.profile_verification import (
    ProfileVerification,
    ProfileVerificationCreate,
    ProfileVerificationGet,
    ProfileVerificationStatusEnum,
)
from src.command.services.profile_verification import (
    InitializeMedia,
    InitializeMediaResponse,
)

router = APIRouter(prefix="/verification", tags=["verification"])


@router.post("/initialize", status_code=201, response_model=InitializeMediaResponse)
async def initialize_upload(
    cmd: FileUploadCommand,
    profile_verification_service: ProfileVerificationServiceDependency,
    user_context: UserContextDependency,
):

    print(cmd)
    return await profile_verification_service.initialize(
        InitializeMedia(
            created_by=user_context.user_id,
            filename=cmd.filename,
            file_size=cmd.file_size,
            content_type=cmd.content_type,
        )
    )


@router.post("/complete", status_code=201, response_model=ProfileVerification)
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


@router.delete("/failed/{media_id}", status_code=204)
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


@router.get("/{id}", status_code=200, response_model=str)
async def get_profile_completion(
    id: str,
    profile_verification_service: ProfileVerificationServiceDependency,
    user_context: UserContextDependency,  # pyright: ignore[reportUnusedParameter]
):
    return await profile_verification_service.get_file_url(
        cmd=ProfileVerificationGet(id=UUID(id))
    )
