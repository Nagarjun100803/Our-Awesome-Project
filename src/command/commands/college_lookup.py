from typing import Annotated

from pydantic import Field

from src.command.commands.base import BaseCmd


class CollegeLookupGet(BaseCmd):
    name: Annotated[str, Field(description="College name")]


class CollegeLookup(BaseCmd):
    college_id: Annotated[int, Field(description="College ID - PK")]
    name: Annotated[str, Field(description="College name")]
    district: Annotated[str, Field(description="College district")]
    state: Annotated[str, Field(description="College state")]
    university_name: Annotated[str, Field(description="College university")]
