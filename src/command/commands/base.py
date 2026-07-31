from pydantic import BaseModel, EmailStr, field_validator
from pydantic.alias_generators import to_camel
from pydantic.config import ConfigDict


class BaseCmd(BaseModel):
    model_config = ConfigDict(
        validate_by_alias=True,
        validate_by_name=True,
        alias_generator=to_camel,
        from_attributes=True,
        extra="ignore",
        str_strip_whitespace=True,
    )

    @field_validator("email", mode="before", check_fields=False)
    @classmethod
    def email_normalize(cls, value: EmailStr) -> EmailStr:
        return value.lower()
