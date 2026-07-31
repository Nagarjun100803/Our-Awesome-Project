from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from authlib.integrations.starlette_client import OAuth
from pydantic.networks import EmailStr

from src.command.commands.providers import ProviderName
from src.settings import settings

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.google.client_id,
    client_secret=settings.google.client_secret,
    server_metadata_url=settings.google.server_metadata_url,
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="microsoft",
    client_id=settings.microsoft.client_id,
    client_secret=settings.microsoft.client_secret,
    server_metadata_url=settings.microsoft.server_metadata_url,
    client_kwargs={"scope": "openid profile User.Read"},
)


@dataclass(frozen=True)
class OAuthProviderConfig:
    """
    Describes how to turn a provider's userinfo dict into (username, email).
    why frozen = True, We cant able to modify the values after the creation of the object.
    """

    name: str
    provider_enum: ProviderName
    extract: Callable[
        [Mapping[str, Any]], tuple[str, EmailStr, str]
    ]  # it takes the fucntion with parameter dict and return type as tuple of str
    # BASED ON THE PROVIDER _extract_google or _extract_mircosoft


def _extract_google(user: Mapping[str, Any]) -> tuple[str, EmailStr, str]:
    return user["name"], user["email"], user["sub"]


def _extract_microsoft(user: Mapping[str, Any]) -> tuple[str, EmailStr, str]:
    email = user["preferred_username"] or user["email"]
    return user["name"], email, user["sub"]


OAUTHPROVIDERS: dict[str, OAuthProviderConfig] = {
    "google": OAuthProviderConfig(
        name="google", provider_enum=ProviderName.GOOGLE, extract=_extract_google
    ),
    "microsoft": OAuthProviderConfig(
        name="microsoft",
        provider_enum=ProviderName.MICROSOFT,
        extract=_extract_microsoft,
    ),
}
