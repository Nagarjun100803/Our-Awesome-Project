from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field

from src.command.commands.base import BaseCmd


class UserRole(StrEnum):
    STUDENT = "student"
    VOLUNTEER = "volunteer"
    ADMIN = "admin"


# Email = Annotated[EmailStr, StringConstraints(strip_whitespace=True, to_lower=True)]


class UserCreate(BaseCmd):
    """User Creation Command"""

    name: Annotated[str, Field(description="User's full name")]
    email: Annotated[EmailStr, Field(description="User's email address")]
    password: Annotated[str | None, Field(description="Account Password")] = None
    role: Annotated[UserRole, Field(description="User's role")] = UserRole.STUDENT
    created_by: Annotated[
        UUID | None, Field(description="User who created this account")
    ] = None
    email_verified: Annotated[
        bool, Field(description="Whether the user's email is verified")
    ] = False


class User(UserCreate):
    """User Core Command"""

    id: Annotated[UUID, Field(description="User's unique identifier")]


class UserUpdate(BaseCmd):
    """User Updation Command"""

    id: Annotated[UUID, Field(description="User's unique identifier")]
    password: Annotated[str | None, Field(description="Account Password")] = None
    role: Annotated[UserRole | None, Field(description="User's role")] = None
    email_verified: Annotated[
        bool | None, Field(description="Whether the user's email is verified")
    ] = None
    updated_by: Annotated[
        UUID | None, Field(description="User who updated this account")
    ] = None


class UserGetByEmail(BaseCmd):
    """Get User Command Using Email"""

    email: Annotated[EmailStr, Field(description="User's email address")]


class UserGetById(BaseCmd):
    """Get User Command Using ID"""

    id: Annotated[UUID, Field(description="User's unique identifier")]
