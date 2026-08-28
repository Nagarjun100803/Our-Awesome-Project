from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BeforeValidator, Field
from pydantic.fields import computed_field

from src.command.commands.base import BaseCmd
from src.command.commands.users import UserRole
from src.query.dto.base import PageMeta, Sort


class UserDTO(BaseCmd):
    id: Annotated[UUID, Field(description="User ID")]
    name: Annotated[str, Field(description="User name")]
    email: Annotated[str, Field(description="User email")]
    role: Annotated[UserRole, Field(description="User role")]
    sequence_number: Annotated[int, Field(description="Sequence number", exclude=True)]
    created_at: Annotated[datetime, Field(description="Created at")]
    last_login: Annotated[datetime | None, Field(description="Last login")] = None
    # display_id: Annotated[str | None, Field(description="Display ID")] = None

    @computed_field
    @property
    def display_id(
        self,
    ) -> str:
        if self.role == UserRole.STUDENT:
            role = "USR"
        elif self.role == UserRole.VOLUNTEER:
            role = "VLR"
        else:
            role = "ADN"
        return f"SETN-{role}-{self.sequence_number:04d}"


class UserFilters(BaseCmd):
    name_or_email: Annotated[str | None, Field(description="User name")] = None
    role: Annotated[UserRole | None, Field(description="User role")] = None
    sort_by_created_at: Annotated[
        Literal["asc", "desc"] | None,
        Field(description="Sort by created at"),
        BeforeValidator(str),
    ] = None
    sort_by_name: Annotated[
        Literal["asc", "desc"] | None,
        Field(description="Sort by name"),
        BeforeValidator(str),
    ] = None
    sort_by_last_login: Annotated[
        Literal["asc", "desc"] | None,
        Field(description="Sort by last login"),
        BeforeValidator(str),
    ] = None

    @property
    def sorts(self) -> list[Sort]:
        list_of_sorts = []
        if self.sort_by_created_at:
            list_of_sorts.append(
                Sort(
                    field="created_at",
                    direction=self.sort_by_created_at,
                    table="users",
                )
            )
        if self.sort_by_name:
            list_of_sorts.append(
                Sort(field="name", direction=self.sort_by_name, table="users")
            )
        if self.sort_by_last_login:
            list_of_sorts.append(
                Sort(
                    field="last_login",
                    direction=self.sort_by_last_login,
                    table="users",
                )
            )
        return list_of_sorts


class UserFiltersWithPagination(PageMeta, UserFilters): ...
