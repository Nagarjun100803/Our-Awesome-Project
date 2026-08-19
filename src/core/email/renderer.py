# src/email/renderer.py

from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    select_autoescape,
)

TEMPLATE_DIR = Path(__file__).parent / "templates"


class EmailTemplateRenderer:
    def __init__(self) -> None:

        self.environment = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            autoescape=select_autoescape(["html", "xml"]),
            undefined=StrictUndefined,
        )

    def render(
        self,
        template_name: str,
        **context,
    ) -> str:

        template = self.environment.get_template(template_name)

        return template.render(**context)
