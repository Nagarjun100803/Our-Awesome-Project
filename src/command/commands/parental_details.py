from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.command.commands.base import BaseCmd


class OccupationEnum(StrEnum):
    GOVT = "government sector"
    PVT = "private sector"
    SELF = "self-employed"
    OTHER = "other"


class AnnualFamilyIncomeEnum(StrEnum):
    """
    | id | label                 | min_amount | max_amount |

    |  1 | Below ₹1,00,000       |          0 |      99999 |
    |  2 | ₹1,00,000 – ₹2,50,000 |     100000 |     249999 |
    |  3 | ₹2,50,000 – ₹5,00,000 |     250000 |     499999 |
    |  4 | ₹5,00,000 – ₹8,00,000 |     500000 |     799999 |
    |  5 | Above ₹8,00,000       |     800000 |       NULL |

    """

    BELOW_100K = "below ₹1,00,000"
    ONE_HUNDRED_TO_250K = "₹1,00,000 – ₹2,50,000"
    TWO_HUNDRED_TO_500K = "₹2,50,000 – ₹5,00,000"
    FIVE_HUNDRED_TO_800K = "₹5,00,000 – ₹8,00,000"
    EIGHT_HUNDRED_PLUS = "above ₹8,00,000"


class FatherDetails(BaseCmd):
    father_name: Annotated[str | None, Field(description="Father's name")] = None
    father_occupation: Annotated[
        OccupationEnum | None, Field(description="Father's occupation")
    ] = None
    father_mobile: Annotated[
        str | None, Field(description="Father's mobile number")
    ] = None


class MotherDetails(BaseCmd):
    mother_name: Annotated[str | None, Field(description="Mother's name")] = None
    mother_occupation: Annotated[
        OccupationEnum | None, Field(description="Mother's occupation")
    ] = None
    mother_mobile: Annotated[
        str | None, Field(description="Mother's mobile number")
    ] = None


class GuardianDetails(BaseCmd):
    guardian_name: Annotated[str | None, Field(description="Guardian's name")] = None
    guardian_occupation: Annotated[
        OccupationEnum | None, Field(description="Guardian's occupation")
    ] = None
    guardian_mobile: Annotated[
        str | None, Field(description="Guardian's mobile number")
    ] = None


class ParentalDetails(FatherDetails, MotherDetails, GuardianDetails, BaseCmd):
    id: Annotated[UUID, Field(description="User ID")]
    annual_family_income: Annotated[
        AnnualFamilyIncomeEnum, Field(description="Annual family income")
    ]


class ParentalDetailsCreate(ParentalDetails):
    created_by: Annotated[UUID, Field(description="Created by")]


class ParentalDetailsUpdate(FatherDetails, MotherDetails, GuardianDetails, BaseCmd):
    id: Annotated[UUID, Field(description="User ID")]
    annual_family_income: Annotated[
        AnnualFamilyIncomeEnum | None, Field(description="Annual family income")
    ] = None
    updated_by: Annotated[UUID, Field(description="Updated by")]


class ParentalDetailsDelete(BaseCmd):
    id: Annotated[UUID, Field(description="User ID")]
    deleted_by: Annotated[UUID, Field(description="Deleted by")]


class ParentalDetailsGet(BaseCmd):
    id: Annotated[UUID, Field(description="User ID")]
