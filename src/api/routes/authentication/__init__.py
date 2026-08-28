from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse

from src.api.dependencies import (
    AuthenticationServiceDependency,
    EmailServiceDependency,
    UserContextDependency,
)
from src.api.schemas.authentication import Login, SignUp
from src.command.commands.users import UserCreate
from src.core.email.models import EmailVerification

from .email_verification import router as email_verification_router
from .oauth import router as oauth_router
from .set_password import router as set_password_router

auth_router = APIRouter(
    prefix="/auth",
)


@auth_router.post("/sign-up", status_code=201, tags=["Local Authentication"])
async def signup(
    cmd: SignUp,
    auth_service: AuthenticationServiceDependency,
    email_service: EmailServiceDependency,
    background_tasks: BackgroundTasks,
    request: Request,
):

    origin = request.headers.get("referer")

    user = await auth_service.signup(
        cmd=UserCreate(name=cmd.name, email=cmd.email, password=cmd.password)
    )
    email_verification_context = await auth_service.generate_email_verification_token(
        email=cmd.email
    )

    email_verification_token = email_verification_context.token

    background_tasks.add_task(
        email_service.send_template_one,
        context=EmailVerification(
            email=cmd.email,
            url=f"{origin}verify-email?token={email_verification_token}",
            name=cmd.name,
        ),
    )

    return JSONResponse(
        content={
            "user": user.model_dump(mode="json"),
            "email_verification_token": email_verification_token,
        }
    )


@auth_router.post("/login", status_code=200, tags=["Local Authentication"])
async def login(cmd: Login, auth_service: AuthenticationServiceDependency):
    access_token = await auth_service.login(cmd=cmd)
    response = JSONResponse(content={"message": "Login Successful"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        samesite="none",
        httponly=True,
        secure=True,
        expires=datetime.now(tz=UTC) + timedelta(days=2),
    )
    return response


@auth_router.post("/logout", status_code=200, tags=["Local Authentication"])
async def logout():
    response = JSONResponse(content={"message": "Logged Out Successfully"})
    response.delete_cookie(
        key="access_token", httponly=True, samesite="none", secure=True
    )
    return response


@auth_router.get("/me", tags=["Local Authentication"])
async def me(user_context: UserContextDependency):
    return user_context


auth_router.include_router(email_verification_router)
auth_router.include_router(oauth_router)
auth_router.include_router(set_password_router)
