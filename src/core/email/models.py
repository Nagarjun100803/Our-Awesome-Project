from typing import Annotated, Self

from pydantic import BaseModel, EmailStr, Field, model_validator


class EmailVerification(BaseModel):
    email: Annotated[EmailStr, Field(description="The email address to verify")]
    url: Annotated[str, Field(description="The verification URL")]
    name: Annotated[str, Field(description="The name of the user")]
    template: Annotated[str, Field(description="The template to use for the email")] = (
        "verify_email.html"
    )
    subject: Annotated[str, Field(description="The subject of the email")] = (
        "Email Verification from Scholarship"
    )
    fallback: Annotated[
        str | None, Field(description="The fallback text to use if the template fails")
    ] = None

    @model_validator(mode="after")
    def fallback_default(self) -> Self:
        if self.fallback is None:
            self.fallback = (
                "Hii "
                + self.name
                + ". Here is the "
                + self.url
                + " to verify your email."
            )
        return self


class SetPassword(BaseModel):
    email: Annotated[
        EmailStr, Field(description="The email address to set the password for")
    ]
    name: Annotated[str, Field(description="The name of the user")]
    url: Annotated[str, Field(description="The Password Reset URL")]
    template: Annotated[str, Field(description="The template to use for the email")] = (
        "set_password.html"
    )
    subject: Annotated[str, Field(description="The subject of the email")] = (
        "Password Reset from Scholarship"
    )
    fallback: Annotated[
        str | None, Field(description="The fallback text to use if the template fails")
    ] = None

    @model_validator(mode="after")
    def fallback_default(self) -> Self:
        if self.fallback is None:
            self.fallback = (
                "Hii "
                + self.name
                + ". Here is the "
                + self.url
                + " to reset your password."
            )
        return self
