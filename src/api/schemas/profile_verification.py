from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.command.commands.base import BaseCmd
from src.command.commands.profile_verification import ProfileVerificationStatusEnum


class VerifySchema(BaseCmd):
    id: Annotated[UUID, Field(description="student id")]
    status: Annotated[
        ProfileVerificationStatusEnum, Field(description="Approved | Rejected")
    ]
    remarks: Annotated[str, Field(description="what is the reason for the status")]
