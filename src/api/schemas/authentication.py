from typing import Annotated, Self

from pydantic import EmailStr, Field
from pydantic.functional_validators import model_validator

from src.command.commands.base import BaseCmd
from src.command.commands.providers import ProviderName
from src.exceptions import NameLengthError, PasswordConfirmMismatchError


class SignUp(BaseCmd):
    """
    Schema for user signup.
    """

    name: Annotated[str, Field(description="Name of the user")]
    email: Annotated[EmailStr, Field(description="Email of the user")]
    password: Annotated[str, Field(description="Password of the user")]
    confirm_password: Annotated[str, Field(description="Confirm password of the user")]

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if len(self.name) < 3:
            raise NameLengthError(message="Name should be at least 3 characters.")
        if self.password != self.confirm_password:
            raise PasswordConfirmMismatchError(
                message="Password and Confirm password should match."
            )
        return self


class Login(BaseCmd):
    """
    Schema for user login.
    """

    email: Annotated[EmailStr, Field(description="Email of the user")]
    password: Annotated[str, Field(description="Password of the user")]


class ForgotPassword(BaseCmd):
    """
    Schema for Forgot password Requesting.
    """

    email: Annotated[EmailStr, Field(description="Email of the user")]


class ResetPassword(BaseCmd):
    """
    Schema for Reset password by clicking the link on email we get the user details from api parameters.
    """

    password: Annotated[str, Field(description="New Password of the user")]
    confirm_password: Annotated[
        str, Field(description="New Confirm password of the user")
    ]

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if self.password != self.confirm_password:
            raise PasswordConfirmMismatchError(
                message="Password and Confirm password should match."
            )
        return self


class ContextFromProvider(BaseCmd):
    """
    Schema for user context from provider.
    Fields:
        1. name: str
        2. email: EmailStr
        3. provider_name: ProviderName
        4. sub: str
    """

    name: Annotated[str, Field(description="Name of the User")]
    email: Annotated[EmailStr, Field(description="Email of the user")]
    provider_name: Annotated[ProviderName, Field(description="Name of the Provider")]
    sub: Annotated[
        str,
        Field(description="Unique identifier of the user which has given by provider"),
    ]
