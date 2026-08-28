from datetime import date, datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.command.commands.base import BaseCmd

"""
id UUID PRIMARY KEY REFERENCES users(id),
dob DATE,
gender VARCHAR(10),
nationality VARCHAR(50),
phone VARCHAR(20),
alternate_phone VARCHAR(20),
street VARCHAR(255),
city VARCHAR(100),
district VARCHAR(70),
state VARCHAR(50),
country VARCHAR(50),
pincode VARCHAR(20),
created_at TIMESTAMPTZ DEFAULT NOW(),
updated_at TIMESTAMPTZ,
created_by UUID REFERENCES users(id),
updated_by UUID REFERENCES users(id)
"""


class GenderType(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ContactInfo(BaseCmd):
    phone: Annotated[str, Field(description="The phone number")]
    alternate_phone: Annotated[
        str | None, Field(description="The alternate phone number")
    ] = None


class AddressInfo(BaseCmd):
    street: Annotated[str, Field(description="The street")]
    city: Annotated[str, Field(description="The city")]
    district: Annotated[str, Field(description="The district")]
    state: Annotated[str, Field(description="The state")]
    country: Annotated[str, Field(description="The country")]
    pincode: Annotated[str, Field(description="The pincode")]


class PersonalDetails(ContactInfo, AddressInfo, BaseCmd):
    id: Annotated[UUID, Field(description="The User ID")]
    dob: Annotated[date, Field(description="The date of birth")]
    gender: Annotated[GenderType, Field(description="The gender")]
    nationality: Annotated[str, Field(description="The nationality")]


class PersonalDetailsCreate(PersonalDetails):
    created_by: Annotated[
        UUID, Field(description="The user who created this personal details record")
    ]


class PersonalDetailsUpdate(BaseCmd):
    id: Annotated[UUID, Field(description="The User ID")]
    dob: Annotated[date | None, Field(description="The date of birth")] = None
    gender: Annotated[GenderType | None, Field(description="The gender")] = None
    nationality: Annotated[str | None, Field(description="The nationality")] = None
    phone: Annotated[str | None, Field(description="The phone number")] = None
    alternate_phone: Annotated[
        str | None, Field(description="The alternate phone number")
    ] = None
    street: Annotated[str | None, Field(description="The street")] = None
    city: Annotated[str | None, Field(description="The city")] = None
    district: Annotated[str | None, Field(description="The district")] = None
    state: Annotated[str | None, Field(description="The state")] = None
    country: Annotated[str | None, Field(description="The country")] = None
    pincode: Annotated[str | None, Field(description="The pincode")] = None
    updated_by: Annotated[
        UUID, Field(description="The user who updated this personal details record")
    ]


class PersonalDetailsGet(BaseCmd):
    id: Annotated[UUID, Field(description="The User ID")]


class PersonalDetailsDelete(BaseCmd):
    id: Annotated[UUID, Field(description="The User ID")]
    deleted_by: Annotated[
        UUID, Field(description="The user who deleted this personal details record")
    ]


if __name__ == "__main__":
    print(
        PersonalDetailsCreate(
            id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
            dob=datetime.fromisoformat("2000-01-01"),
            gender=GenderType.MALE,
            nationality="Indian",
            created_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
            phone="+91 987654321",
            alternate_phone=None,
            street="Something Street",
            city="Chennai",
            district="Chennai",
            state="Tamil Nadu",
            country="India",
            pincode="600091",
        )
    )
