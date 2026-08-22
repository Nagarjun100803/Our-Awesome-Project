from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

from src.api.dependencies import AuthenticationServiceDependency, EmailServiceDependency
from src.api.schemas.authentication import ForgotPassword, ResetPassword
from src.command.commands.authentication import ResetPasswordByToken
from src.core.email.models import SetPassword

router = APIRouter(tags=["set-password"])


@router.post(
    "/generate-set-password-token",
    status_code=200,
)
async def generate_set_password_token(
    cmd: ForgotPassword,
    auth_service: AuthenticationServiceDependency,
    email_service: EmailServiceDependency,
    background_tasks: BackgroundTasks,
):
    forgot_password_context = await auth_service.generate_set_password_token(cmd=cmd)

    background_tasks.add_task(
        email_service.send_template_one,
        context=SetPassword(
            email=cmd.email,
            url=f"http://localhost:5173/set-password?token={forgot_password_context.token}",
            name=forgot_password_context.name,
        ),
    )

    return JSONResponse(
        content={
            "message": f"Hi {forgot_password_context.name}, Password Reset link sent to your mail. ",
            "reset_token": forgot_password_context.token,
        }
    )


@router.post("/set-password", status_code=200)
async def set_password(
    token: str, cmd: ResetPassword, auth_service: AuthenticationServiceDependency
):
    _ = await auth_service.set_password(
        cmd=ResetPasswordByToken(
            token=token, password=cmd.password, confirm_password=cmd.confirm_password
        )
    )
    return JSONResponse(content={"message": "Password Reset Successfully"})
