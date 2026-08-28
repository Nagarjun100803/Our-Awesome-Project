from fastapi import APIRouter

from src.api.dependencies import PersonalDetailsServiceDependency, UserContextDependency
from src.api.schemas.profile_completion import PersonalDetailsSchema
from src.command.commands.personal_details import PersonalDetails, PersonalDetailsCreate

router = APIRouter(prefix="/personal", tags=["personal details"])


@router.post("/", status_code=201, response_model=PersonalDetails)
async def create_personal_details(
    cmd: PersonalDetailsSchema,
    personal_service: PersonalDetailsServiceDependency,
    user_context: UserContextDependency,
):

    return await personal_service.create(
        PersonalDetailsCreate(
            id=user_context.user_id,
            created_by=user_context.user_id,
            **cmd.model_dump(mode="json"),  # pyright: ignore[reportAny]
        )
    )
