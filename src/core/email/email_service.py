# src/email/service.py

from src.core.email.models import EmailVerification, SetPassword
from src.core.email.provider import (
    EmailBody,
    EmailMessage,
    SMTPEmailProvider,
)
from src.core.email.renderer import EmailTemplateRenderer


class EmailService:
    def __init__(
        self,
        provider: SMTPEmailProvider,
        renderer: EmailTemplateRenderer,
    ) -> None:

        self.provider = provider
        self.renderer = renderer

    async def send_template_one(
        self,
        context: EmailVerification | SetPassword,
    ) -> None:

        html = self.renderer.render(
            context.template,
            subject=context.subject,
            **context.model_dump(exclude={"template", "subject", "email", "fallback"}),
        )

        message = EmailMessage(
            to=context.email,
            subject=context.subject,
            body=EmailBody(
                text=context.fallback,
                html=html,
            ),
        )

        await self.provider.send(message)


async def main():
    service = EmailService(
        provider=SMTPEmailProvider(),
        renderer=EmailTemplateRenderer(),
    )

    await service.send_template_one(
        context=EmailVerification(
            template="verify_email.html",
            email="arulsampathcyr@gmail.com",
            url="http://localhost:8000/docs",
            name="Arul S",
        ),
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
