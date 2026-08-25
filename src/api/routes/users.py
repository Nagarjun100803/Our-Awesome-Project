from fastapi import APIRouter, Request

from src.api.dependencies import UserContextDependency, UserServiceDependency
from src.api.schemas.users import UserCreateSchema
from src.command.commands.users import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def create_user(
    cmd: UserCreateSchema,
    user_service: UserServiceDependency,
    request: Request,
    user_context: UserContextDependency,
):
    origin = request.headers.get("referer")
    return await user_service.register(
        UserCreate(
            name=cmd.name,
            email=cmd.email,
            role=cmd.role,
            email_verified=True,
            created_by=user_context.user_id,
        ),
        origin=origin or "",
    )
