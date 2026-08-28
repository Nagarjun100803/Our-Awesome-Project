from fastapi import APIRouter, Depends

from src.api.dependencies import (
    UserContextDependency,
    VerifyProfileCompletionServiceDependency,
    require_role,
)
from src.api.schemas.profile_completion import ProfileCompletionStatus
from src.command.commands.users import UserRole

from .academic import router as academic_router
from .lookup import router as lookup_router
from .parental import router as parental_router
from .personal import router as personal_router
from .verification import router as verification_router

router = APIRouter(
    prefix="/profile",
    dependencies=[Depends(require_role(UserRole.STUDENT))],
)

router.include_router(personal_router)
router.include_router(parental_router)
router.include_router(academic_router)
router.include_router(verification_router)
router.include_router(lookup_router)


@router.get(
    "/status", tags=["Profile"], status_code=200, response_model=ProfileCompletionStatus
)
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
