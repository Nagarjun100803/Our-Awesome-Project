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

        self.provider: SMTPEmailProvider = provider
        self.renderer: EmailTemplateRenderer = renderer

    async def send_template_one(
        self,
        context: EmailVerification | SetPassword,
    ) -> None:

        html = self.renderer.render(  # pyright: ignore[reportUnknownMemberType]
            context.template,
            subject=context.subject,
            **context.model_dump(exclude={"template", "subject", "email", "fallback"}),  # pyright: ignore[reportAny]
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
