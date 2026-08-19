# src/email/providers/smtp.py

from email.message import EmailMessage as SMTPMessage

# src/email/models.py
from typing import Annotated, Self

import aiosmtplib
from pydantic import BaseModel, EmailStr, model_validator
from pydantic.fields import Field

from src.settings import settings


class EmailBody(BaseModel):
    text: Annotated[str | None, Field("Email body text")] = None
    html: Annotated[str | None, Field("Email body HTML")] = None

    @model_validator(mode="after")
    def validate_body(self) -> Self:

        if self.text is None and self.html is None:
            raise ValueError("Either text or html must be provided")

        return self


class EmailMessage(BaseModel):
    to: Annotated[EmailStr, Field("Email recipients")]
    subject: Annotated[str, Field("Email subject")]
    body: Annotated[EmailBody, Field("Email body")]


class SMTPEmailProvider:
    async def send(
        self,
        message: EmailMessage,
    ) -> None:

        email = SMTPMessage()

        # Sender
        email["From"] = f"{settings.email.from_name} <{settings.email.from_email}>"

        # Recipients
        # email["To"] = ", ".join(str(address) for address in message.to)
        #
        email["To"] = message.to

        # Subject
        email["Subject"] = message.subject

        # HTML alternative
        if message.body.html:
            email.set_content(
                message.body.html,
                subtype="html",
            )
        else:
            email.add_alternative(
                message.body.text,
                subtype="plain",
            )

        # Send
        await aiosmtplib.send(
            email,
            hostname=settings.email.smtp_host,
            port=settings.email.smtp_port,
            username=(settings.email.smtp_username),
            password=(settings.email.smtp_password.get_secret_value()),
            start_tls=settings.email.start_tls,
        )


async def main():
    email_provider = SMTPEmailProvider()
    await email_provider.send(
        EmailMessage(
            to="arulsampathcyr@gmail.com",
            subject="Account Verification",
            body=EmailBody(text="Click Here"),
        )
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
