from typing import Annotated

from pydantic import Field

from src.command.commands.base import BaseCmd
from src.command.commands.users import UserRole


class UserCreateSchema(BaseCmd):
    name: Annotated[str, Field(description="User's name")]
    email: Annotated[str, Field(description="User's email")]
    role: Annotated[UserRole, Field(description="User's role")]
