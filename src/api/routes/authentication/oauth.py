from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from src.api.dependencies import AuthenticationServiceDependency
from src.api.schemas.authentication import ContextFromProvider
from src.command.commands.providers import ProviderName
from src.core.security.oauth2 import OAUTHPROVIDERS, oauth
from src.settings import settings

router = APIRouter(tags=["oauth"])


@router.get("/google")
async def google_login(request: Request):  # pyright: ignore[reportUnknownParameterType]
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        request,
        redirect_uri,
        access_type="offline",
    )


@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request, auth_service: AuthenticationServiceDependency
):
    provider_name = "google"
    provider_config = OAUTHPROVIDERS[provider_name]

    client = oauth.create_client(name=provider_name)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

    token = await client.authorize_access_token(request)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    user = token["userinfo"]  # pyright: ignore[reportUnknownVariableType]

    name, email, sub = provider_config.extract(user)  # pyright: ignore[reportUnknownArgumentType]

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


@router.get("/microsoft")
async def microsoft_login(request: Request):  # pyright: ignore[reportUnknownParameterType]
    redirect_uri = request.url_for("microsoft_callback")
    return await oauth.microsoft.authorize_redirect(  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
        request,
        redirect_uri,
        access_type="offline",
    )


@router.get("/microsoft/callback", name="microsoft_callback")
async def microsoft_callback(
    request: Request, auth_service: AuthenticationServiceDependency
):
    provider_name = "microsoft"
    provider_config = OAUTHPROVIDERS[provider_name]

    client = oauth.create_client(name=provider_name)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    token = await client.authorize_access_token(request, claims_options={})  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    user = token["userinfo"]  # pyright: ignore[reportUnknownVariableType]

    name, email, sub = provider_config.extract(user)  # pyright: ignore[reportUnknownArgumentType]

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
