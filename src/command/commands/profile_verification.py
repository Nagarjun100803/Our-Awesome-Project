from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.command.commands.base import BaseCmd


class ProfileVerificationStatusEnum(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ProfileVerification(BaseCmd):
    id: Annotated[UUID, Field(description="Profile verification - User ID")]
    media_id: Annotated[UUID, Field(description="Profile verification - Media ID")]
    status: Annotated[
        ProfileVerificationStatusEnum,
        Field(
            description="Profile verification - Status",
            default=ProfileVerificationStatusEnum.PENDING,
        ),
    ]
    remarks: Annotated[
        str | None, Field(description="Profile verification - Remarks")
    ] = None
    verified_by: Annotated[
        UUID | None, Field(description="Profile verification - Verified by")
    ] = None


class ProfileVerificationCreate(ProfileVerification):
    created_by: Annotated[UUID, Field(description="Profile verification - Created by")]


class ProfileVerificationUpdate(BaseCmd):
    id: Annotated[UUID, Field(description="user_id")]
    status: Annotated[
        ProfileVerificationStatusEnum,
        Field(description="Profile verification - Status"),
    ]
    remarks: Annotated[str, Field(description="Profile verification - Remarks")]
    verified_by: Annotated[UUID, Field(description="Profile verification - Updated by")]
    updated_by: Annotated[UUID, Field(description="Profile verification - Updated by")]


class ProfileVerificationDelete(BaseCmd):
    id: Annotated[UUID, Field(description="Profile verification - User ID")]
    deleted_by: Annotated[UUID, Field(description="Profile verification - Deleted by")]


class ProfileVerificationGet(BaseCmd):
    id: Annotated[UUID, Field(description="Profile verification - User ID")]


class ProfileVerify(BaseCmd):
    id: Annotated[UUID, Field(description="student id")]
    status: Annotated[
        ProfileVerificationStatusEnum, Field(description="Approved | Rejected")
    ]
    remarks: Annotated[str, Field(description="what is the reason for the status")]
    verified_by: Annotated[UUID, Field(description="who done this verification")]
