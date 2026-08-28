from fastapi import APIRouter

from src.api.dependencies import ParentalDetailsServiceDependency, UserContextDependency
from src.api.schemas.profile_completion import ParentalDetailsSchema
from src.command.commands.parental_details import ParentalDetails

router = APIRouter(prefix="/parental", tags=["parental details"])


@router.post("/", status_code=201, response_model=ParentalDetails)
async def create_parental_details(
    cmd: ParentalDetailsSchema,
    parental_service: ParentalDetailsServiceDependency,
    user_context: UserContextDependency,
):
    return await parental_service.create(cmd.to_create(user_id=user_context.user_id))
