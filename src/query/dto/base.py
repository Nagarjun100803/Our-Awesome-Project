from math import ceil
from typing import Annotated, Literal

from pydantic import BeforeValidator, Field, field_validator
from pydantic.fields import computed_field
from pypika import Table

from src.command.commands.base import BaseCmd


class PageMeta(BaseCmd):
    page: Annotated[int, Field(description="Page", gt=0)] = 1
    limit: Annotated[
        Literal[10, 15, 20, 25], Field(description="Limit"), BeforeValidator(int)
    ] = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class Sort(BaseCmd):
    field: Annotated[
        Literal["last_login", "created_at", "name", "email", "submitted_on"],
        Field(description="Field to sort by"),
    ]
    direction: Annotated[str, Field(description="Sort direction")]
    table: Annotated[
        Literal["users", "profile_verification"], Field(description="Table to sort by")
    ]

    @field_validator("direction", mode="before")
    @classmethod
    def normalize_direction(cls, value: str) -> str:
        return value.upper()


class Paginated[T](BaseCmd):
    data: list[T]
    page: int
    limit: int
    total_items: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return ceil(self.total_items / self.limit) if self.total_items > 0 else 0


user_table = Table("users")
profile_table = Table("profile_verification")
