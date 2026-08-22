from datetime import date
from typing import Annotated, Self
from uuid import UUID

from pydantic import Field, model_validator

from src.command.commands.academic_details import (
    GradingSystemEnum,
    LevelOfEducationEnum,
)
from src.command.commands.base import BaseCmd
from src.command.commands.parental_details import (
    AnnualFamilyIncomeEnum,
    OccupationEnum,
    ParentalDetailsCreate,
)
from src.command.commands.personal_details import GenderType
from src.exceptions import ParentalDetailsError


class PersonalDetailsSchema(BaseCmd):
    dob: Annotated[date, Field(description="The date of birth")]
    gender: Annotated[GenderType, Field(description="The gender")]
    nationality: Annotated[str, Field(description="The nationality")]
    street: Annotated[str, Field(description="The street")]
    city: Annotated[str, Field(description="The city")]
    district: Annotated[str, Field(description="The district")]
    state: Annotated[str, Field(description="The state")]
    country: Annotated[str, Field(description="The country")]
    pincode: Annotated[str, Field(description="The pincode", pattern=r"^\d{6}$")]
    phone: Annotated[str, Field(description="The phone number")]
    alternate_phone: Annotated[
        str | None, Field(description="The alternate phone number")
    ] = None


class GenericDetails(BaseCmd):
    name: Annotated[str, Field(description="The name")]
    occupation: Annotated[OccupationEnum, Field(description="The occupation")]
    mobile: Annotated[
        str, Field(description="The mobile number", pattern=r"^\+91[6-9]\d{9}$")
    ]


class ParentalDetailsSchema(BaseCmd):
    father: Annotated[
        GenericDetails | None, Field(description="The father details")
    ] = None
    mother: Annotated[
        GenericDetails | None, Field(description="The mother details")
    ] = None
    guardian: Annotated[
        GenericDetails | None, Field(description="The guardian details")
    ] = None

    annual_family_income: Annotated[
        AnnualFamilyIncomeEnum, Field(description="The family annual income")
    ]

    @model_validator(mode="after")
    def validate_parental_details(self) -> Self:
        if self.father is None and self.mother is None and self.guardian is None:
            raise ParentalDetailsError("At least one parental detail is required")
        if self.father and self.guardian:
            raise ParentalDetailsError("Only one of father or guardian can be provided")
        if self.mother and self.guardian:
            raise ParentalDetailsError("Only one of mother or guardian can be provided")
        if self.father and self.mother and self.guardian:
            raise ParentalDetailsError(
                "Only father, mother, or guardian can be provided"
            )
        return self

    def to_create(self, user_id: UUID) -> ParentalDetailsCreate:
        return ParentalDetailsCreate(
            id=user_id,
            created_by=user_id,
            father_name=self.father.name if self.father else None,
            father_occupation=self.father.occupation if self.father else None,
            father_mobile=self.father.mobile if self.father else None,
            mother_name=self.mother.name if self.mother else None,
            mother_occupation=self.mother.occupation if self.mother else None,
            mother_mobile=self.mother.mobile if self.mother else None,
            guardian_name=self.guardian.name if self.guardian else None,
            guardian_occupation=self.guardian.occupation if self.guardian else None,
            guardian_mobile=self.guardian.mobile if self.guardian else None,
            annual_family_income=self.annual_family_income,
        )


class AcademicCreateSchema(BaseCmd):
    level_of_education: Annotated[
        LevelOfEducationEnum,
        Field(
            description="Level of Education e.g., 10th, 12th/diploma, undergraduate, postgraduate, research/PhD"
        ),
    ]
    institution_name: Annotated[
        str, Field(description="Institution Name e.g., School, College")
    ]
    board_university: Annotated[
        str, Field(description="Board/University e.g., CBSE, ICSE, State University")
    ]
    course_stream_specialization: Annotated[
        str | None,
        Field(
            description="Course Stream/Specialization e.g., Computer Science, Engineering, Business"
        ),
    ] = None
    year_of_passing: Annotated[
        str, Field(description="Year of Passing e.g., 2020, 2021")
    ]
    register_number: Annotated[
        str | None, Field(description="Register Number e.g., ")
    ] = None
    grading_system: Annotated[
        GradingSystemEnum | None,
        Field(description="Grading System e.g., percentage, cgpa"),
    ] = None
    score: Annotated[
        str | None,
        Field(description="Score e.g., 90.5, 85.0, 9.0", max_length=5),
    ] = None
    current_semester: Annotated[
        int | None, Field(description="Current Semester e.g., 1, 2, 3", le=20)
    ] = None
    currently_enrolled: Annotated[
        bool,
        Field(
            description="The field indicates whether the student is currently enrolled in the course"
        ),
    ] = False


class AcademicUpdateSchema(BaseCmd):
    course_stream_specialization: Annotated[
        str | None,
        Field(
            description="Course Stream/Specialization e.g., Computer Science, Engineering, Business"
        ),
    ] = None
    register_number: Annotated[
        str | None, Field(description="Register Number e.g., ")
    ] = None
    grading_system: Annotated[
        GradingSystemEnum | None,
        Field(description="Grading System e.g., percentage, cgpa"),
    ] = None
    score: Annotated[
        str | None,
        Field(description="Score e.g., 90.5, 85.0, 9.0", max_length=5),
    ] = None
    current_semester: Annotated[
        int | None, Field(description="Current Semester e.g., 1, 2, 3", le=20)
    ] = None
    currently_enrolled: Annotated[
        bool | None,
        Field(
            description="The field indicates whether the student is currently enrolled in the course"
        ),
    ] = None


class ProfileCompletionStatus(BaseCmd):
    personal_details: Annotated[
        bool, Field(description="Used to Check the personal details completed")
    ]
    academic_details: Annotated[
        bool, Field(description="Used to Check the academic details completed")
    ]
    parental_details: Annotated[
        bool, Field(description="Used to Check the parental details completed")
    ]
    id_uploaded: Annotated[bool, Field(description="Used to Check the ID uploaded")]


class PincodeLookupResponse(BaseCmd):
    pincode: Annotated[str, Field(description="The pincode")]
    state: Annotated[str, Field(description="The state")]
    district: Annotated[str, Field(description="The district")]
    city: Annotated[
        list[str], Field(description="List of localities/areas under this pincode")
    ]


class CollegeLookupResponse(BaseCmd):
    name: Annotated[str, Field(description="The name of the college")]
    university: Annotated[str, Field(description="The university of the college")]


class FileUploadCommand(BaseCmd):
    filename: Annotated[str, Field(description="The name of the file")]
    file_size: Annotated[int, Field(description="The size of the file")]
    content_type: Annotated[
        str, Field(description="The content type of the file like application/pdf")
    ]
