from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import EmailStr

from src.api.dependencies import (
    AuthenticationServiceDependency,
    EmailServiceDependency,
    UserContextDependency,
)
from src.api.schemas.authentication import (
    ContextFromProvider,
    ForgotPassword,
    Login,
    ResetPassword,
    SignUp,
)
from src.command.commands.authentication import ResetPasswordByToken, VerifyEmailByToken
from src.command.commands.providers import ProviderName
from src.command.commands.users import UserCreate
from src.core.email.models import EmailVerification, SetPassword
from src.core.security.oauth2 import OAUTHPROVIDERS, oauth
from src.settings import settings

auth_router = APIRouter(tags=["Authentication"], prefix="/auth")


@auth_router.post("/sign-up", status_code=201)
async def signup(
    cmd: SignUp,
    auth_service: AuthenticationServiceDependency,
    email_service: EmailServiceDependency,
    background_tasks: BackgroundTasks,
):
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
            url=f"http://localhost:5173/verify-email?token={email_verification_token}",
            name=cmd.name,
        ),
    )

    return JSONResponse(
        content={
            "user": user.model_dump(mode="json"),
            "email_verification_token": email_verification_token,
        }
    )


@auth_router.post("/login", status_code=200)
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


@auth_router.post(
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


@auth_router.post("/set-password", status_code=200)
async def set_password(
    token: str, cmd: ResetPassword, auth_service: AuthenticationServiceDependency
):
    await auth_service.set_password(
        cmd=ResetPasswordByToken(
            token=token, password=cmd.password, confirm_password=cmd.confirm_password
        )
    )
    return JSONResponse(content={"message": "Password Reset Successfully"})


@auth_router.post("/resend-email-verification/", status_code=200)
async def resend_email_verification(
    email: EmailStr,
    auth_service: AuthenticationServiceDependency,
    email_service: EmailServiceDependency,
    background_tasks: BackgroundTasks,
):
    email_verification_context = await auth_service.generate_email_verification_token(
        email=email
    )

    background_tasks.add_task(
        email_service.send_template_one,
        context=EmailVerification(
            email=email,
            url=f"http://localhost:5173/verify-email?token={email_verification_context.token}",
            name=email_verification_context.name,
        ),
    )

    return {"email_verification_token": email_verification_context.token}


@auth_router.post("/verify-email", status_code=200)
async def verify_email(token: str, auth_service: AuthenticationServiceDependency):
    access_token = await auth_service.verify_email(cmd=VerifyEmailByToken(token=token))
    response = JSONResponse(content={"message": "Email Verified Successfully"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        samesite="none",
        httponly=True,
        secure=True,
        expires=datetime.now(tz=UTC) + timedelta(days=2),
    )
    return response


@auth_router.post("/logout", status_code=200)
async def logout():
    response = JSONResponse(content={"message": "Logged Out Successfully"})
    response.delete_cookie(
        key="access_token", httponly=True, samesite="none", secure=True
    )
    return response


@auth_router.get("/me")
async def me(user_context: UserContextDependency):
    return user_context


"""
OAUTH LOGIN
"""


@auth_router.get("/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
    )


@auth_router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request, auth_service: AuthenticationServiceDependency
):
    provider_name = "google"
    provider_config = OAUTHPROVIDERS[provider_name]

    client = oauth.create_client(name=provider_name)

    token = await client.authorize_access_token(request)

    user = token["userinfo"]

    name, email, sub = provider_config.extract(user)

    access_token = await auth_service.continue_with_oauth(
        cmd=ContextFromProvider(
            provider_name=ProviderName.GOOGLE,
            name=name,
            email=email,
            sub=sub,
        )
    )

    response = RedirectResponse(url=settings.frontend.url, status_code=302)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response


@auth_router.get("/microsoft")
async def microsoft_login(request: Request):
    redirect_uri = request.url_for("microsoft_callback")
    return await oauth.microsoft.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
    )


@auth_router.get("/microsoft/callback", name="microsoft_callback")
async def microsoft_callback(
    request: Request, auth_service: AuthenticationServiceDependency
):
    provider_name = "microsoft"
    provider_config = OAUTHPROVIDERS[provider_name]

    client = oauth.create_client(name=provider_name)

    token = await client.authorize_access_token(request, claims_options={})

    user = token["userinfo"]

    name, email, sub = provider_config.extract(user)

    access_token = await auth_service.continue_with_oauth(
        cmd=ContextFromProvider(
            provider_name=ProviderName.MICROSOFT,
            name=name,
            email=email,
            sub=sub,
        )
    )

    response = RedirectResponse(url=settings.frontend.url, status_code=302)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response
