from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from src.api.dependencies import AuthenticationServiceDependency, EmailServiceDependency
from src.command.commands.authentication import VerifyEmailByToken
from src.core.email.models import EmailVerification

router = APIRouter(
    tags=["Email Verification"],
)


@router.post("/resend-email-verification", status_code=200)
async def resend_email_verification(
    email: EmailStr,
    auth_service: AuthenticationServiceDependency,
    email_service: EmailServiceDependency,
    background_tasks: BackgroundTasks,
    request: Request,
):
    origin = request.headers.get("referer")
    email_verification_context = await auth_service.generate_email_verification_token(
        email=email
    )

    background_tasks.add_task(
        email_service.send_template_one,
        context=EmailVerification(
            email=email,
            url=f"{origin}verify-email?token={email_verification_context.token}",
            name=email_verification_context.name,
        ),
    )

    return {"email_verification_token": email_verification_context.token}


@router.post("/verify-email", status_code=200)
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
