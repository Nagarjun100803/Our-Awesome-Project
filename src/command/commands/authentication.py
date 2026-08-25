from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field

from src.api.schemas.authentication import ResetPassword
from src.command.commands.base import BaseCmd
from src.command.commands.users import UserRole


class ResetPasswordByToken(ResetPassword):
    """
    Command with token to reset password.
    fields: Password, Confirm Password, token(send in mail)
    """

    token: Annotated[str, Field(description="Token received from user email")]


class VerifyEmailByToken(BaseCmd):
    """
    Command to verify email by token.
    """

    token: Annotated[str, Field(description="Token received from user email")]


class GetUserByToken(BaseCmd):
    """
    Command to get user by token.
    """

    token: Annotated[str, Field(description="Token received from user email")]


class ResetPasswordContext(BaseCmd):
    """
    Context for resetting password.
    """

    name: Annotated[str, Field(description="name of the user")]
    token: Annotated[str, Field(description="Token received from user email")]


class EmailVerificationContext(BaseCmd):
    """
    Context for resending verification email.
    """

    name: Annotated[str, Field(description="name of the user")]
    token: Annotated[str, Field(description="Token received from user email")]


class UserContext(BaseCmd):
    """Context of the authenticated user"""

    user_id: Annotated[UUID, Field(description="User ID")]
    username: Annotated[str, Field(description="Username")]
    email: Annotated[EmailStr, Field(description="Email address")]
    role: Annotated[UserRole, Field(description="User role")]


class UpdateLastLogin(BaseCmd):
    """
    Command to update last login.
    """

    user_id: Annotated[UUID, Field(description="User ID")]
