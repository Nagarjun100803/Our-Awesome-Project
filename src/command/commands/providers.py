from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.command.commands.base import BaseCmd


class ProviderName(StrEnum):
    """
    Enum representing the name of the provider.
    """

    GOOGLE = "google"
    MICROSOFT = "microsoft"


class Provider(BaseCmd):
    """
    Core Provider Representation
    Fields:
        1. name: ProviderName
        2. user_id: UUID
        3. sub: str
    """

    name: Annotated[
        ProviderName, Field(description="Name of the provider ex: google, microsoft")
    ]
    user_id: Annotated[
        UUID,
        Field(description="User Id Based on that we check use has particular provider"),
    ]
    sub: Annotated[
        str,
        Field(description="Subject identifier from the provider"),
    ]


class ProviderCreate(Provider):
    """
    Create a new provider.
    Fields:
        1. name: ProviderName
        2. user_id: UUID
        3. sub: str
    """


class ProviderGet(BaseCmd):
    """
    Get a provider.
    Fields:
        1. name: ProviderName
        2. user_id: UUID
    """

    name: Annotated[
        ProviderName, Field(description="Name of the provider ex: google, microsoft")
    ]
    user_id: Annotated[
        UUID,
        Field(description="User Id Based on that we check use has particular provider"),
    ]


class ProviderDelete(BaseCmd):
    """
    Delete a provider.
    Fields:
        1. name: ProviderName
        2. user_id: UUID
    """

    name: Annotated[
        ProviderName, Field(description="Name of the provider ex: google, microsoft")
    ]
    user_id: Annotated[
        UUID,
        Field(description="User Id Based on that we check use has particular provider"),
    ]
