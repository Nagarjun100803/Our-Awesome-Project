from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.command.commands.base import BaseCmd

"""
CREATE TABLE IF NOT EXISTS media (
    id UUID PRIMARY KEY default gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    storage_provider VARCHAR(255) NOT NULL,
    storage_key VARCHAR(255) NOT NULL,
    content_type VARCHAR(255) NOT NULL,
    file_size INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(255) NOT NULL DEFAULT 'pending'
);
"""


class MediaStatusEnum(StrEnum):
    PENDING = "pending"
    FAILED = "failed"
    UPLOADED = "uploaded"


class Media(BaseCmd):
    id: Annotated[UUID | None, Field(description="Media ID")] = None
    filename: Annotated[str, Field(description="File name")]
    storage_provider: Annotated[str, Field(description="Storage provider")]
    storage_key: Annotated[
        str, Field(description="Storage key path of the file which stored in storage")
    ]
    file_size: Annotated[int, Field(description="File size")]
    content_type: Annotated[str, Field(description="Content type")]
    status: Annotated[
        MediaStatusEnum,
        Field(description="Media status", default=MediaStatusEnum.PENDING),
    ]


class MediaCreate(Media):
    created_by: Annotated[UUID, Field(description="User ID")]


class MediaUpdate(BaseCmd):
    id: Annotated[UUID, Field(description="Media ID")]
    status: Annotated[
        MediaStatusEnum,
        Field(description="Media status"),
    ]
    updated_by: Annotated[UUID, Field(description="User ID")]


class MediaGet(BaseCmd):
    id: Annotated[UUID, Field(description="Media ID")]


class MediaDelete(BaseCmd):
    id: Annotated[UUID, Field(description="Media ID")]
    deleted_by: Annotated[UUID, Field(description="User ID")]
