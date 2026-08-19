"""
CREATE TABLE IF NOT EXISTS educational_details(
    id UUID REFERENCES users(id),
    level_of_education VARCHAR(100) NOT NULL,
    institution_name VARCHAR(255) NOT NULL,
    board_university VARCHAR(255) NOT NULL,
    course_stream_specialization VARCHAR(255),
    year_of_passing VARCHAR(5) NOT NULL,
    register_number VARCHAR(100),
    current_semester NUMERIC(2),
    grading_system VARCHAR(50),
    score NUMERIC(3,3),
    currently_enrolled BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES users(id) NOT NULL,
    updated_by UUID REFERENCES users(id),
    deleted_by UUID REFERENCES users(id)
);
"""

from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.command.commands.base import BaseCmd


class LevelOfEducationEnum(StrEnum):
    SCHOOL_10TH = "10th Grade"
    DIPLOMA_12TH = "12th or Diploma"
    UNDERGRADUATE = "Undergraduate"
    POSTGRADUATE = "Postgraduate"
    RESEARCH_PHD = "Research or PhD"


class GradingSystemEnum(StrEnum):
    PERCENTAGE = "percentage"
    CGPA = "cgpa"


class AcademicDetails(BaseCmd):
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
        str, Field(description="Year of Passing e.g., 2020, 2021", max_length=4)
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
        Field(description="Score e.g., 90.5, 85.0, 9.0"),
    ] = None
    current_semester: Annotated[
        int | None, Field(description="Current Semester e.g., 1, 2, 3")
    ] = None
    currently_enrolled: Annotated[
        bool,
        Field(
            description="The field indicates whether the student is currently enrolled in the course"
        ),
    ] = False


class AcademicDetailsCreate(AcademicDetails):
    id: Annotated[UUID, Field(description="User Id")]
    created_by: Annotated[
        UUID,
        Field(
            description="The field indicates the user who created the academic details e.g., Admin, Volunteer, or User"
        ),
    ]


class AcademicDetailsGet(BaseCmd):
    id: Annotated[UUID, Field(description="User Id")]
    level_of_education: Annotated[
        LevelOfEducationEnum,
        Field(description="Level of Education e.g., Bachelor, Master, PhD"),
    ]


class AcademicDetailsGetAll(BaseCmd):
    id: Annotated[UUID, Field(description="User Id")]


class AcademicDetailsDelete(BaseCmd):
    id: Annotated[UUID, Field(description="User Id")]
    deleted_by: Annotated[
        UUID,
        Field(
            description="The field indicates the user who deleted the academic details e.g., Admin, Volunteer, or User"
        ),
    ]
    level_of_education: Annotated[
        LevelOfEducationEnum,
        Field(description="Level of Education e.g., Bachelor, Master, PhD"),
    ]


class AcademicDetailsDeleteAll(BaseCmd):
    id: Annotated[UUID, Field(description="User Id")]
    deleted_by: Annotated[
        UUID,
        Field(
            description="The field indicates the user who deleted the academic details e.g., Admin, Volunteer, or User"
        ),
    ]


class AcademicDetailsUpadate(BaseCmd):
    id: Annotated[UUID, Field(description="User Id")]
    level_of_education: Annotated[
        LevelOfEducationEnum,
        Field(
            description="Level of Education e.g., 10th, 12th/diploma, undergraduate, postgraduate, research/PhD"
        ),
    ]
    institution_name: Annotated[
        str | None, Field(description="Institution Name e.g., School, College")
    ] = None
    board_university: Annotated[
        str | None,
        Field(description="Board/University e.g., CBSE, ICSE, State University"),
    ] = None
    year_of_passing: Annotated[
        str | None, Field(description="Year of Passing e.g., 2020, 2021", max_length=4)
    ] = None
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
        Field(description="Score e.g., 90.5, 85.0, 9.0"),
    ] = None
    current_semester: Annotated[
        int | None, Field(description="Current Semester e.g., 1, 2, 3")
    ] = None
    currently_enrolled: Annotated[
        bool | None,
        Field(
            description="The field indicates whether the student is currently enrolled in the course"
        ),
    ] = None

    updated_by: Annotated[UUID, Field(description="Updated by")]
