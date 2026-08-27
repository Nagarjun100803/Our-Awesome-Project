from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, computed_field

from src.command.commands.academic_details import LevelOfEducationEnum
from src.command.commands.base import BaseCmd
from src.command.commands.users import UserRole
from src.query.dto.base import PageMeta, Sort, profile_table, user_table


class VerificationDTO(BaseCmd):
    id: Annotated[UUID, Field(description="User ID")]
    name: Annotated[str, Field(description="User name")]
    sequence_number: Annotated[int, Field(description="Sequence number")]
    role: Annotated[UserRole, Field(description="Role")]
    institution_name: Annotated[str, Field(description="Institution name")]
    level_of_education: Annotated[
        LevelOfEducationEnum, Field(description="Level of education")
    ]
    course: Annotated[str | None, Field(description="Courses")] = None
    semester: Annotated[int | None, Field(description="Semester")] = None
    submitted_on: Annotated[datetime, Field(description="Submitted at")]

    @computed_field
    @property
    def course_or_level_of_education(self) -> str:
        if self.course:
            return self.course
        return self.level_of_education.value

    @computed_field
    @property
    def display_id(
        self,
    ) -> str:
        if self.role == UserRole.STUDENT:
            role = "USR"
        elif self.role == UserRole.VOLUNTEER:
            role = "VLR"
        else:
            role = "ADN"
        return f"SETN-{role}-{self.sequence_number:04d}"


class VolunteerDetails(BaseCmd):
    volunteer_id: Annotated[UUID, Field(description="User ID")]
    volunteer_name: Annotated[str, Field(description="User name")]
    volunteer_sequence_number: Annotated[int, Field(description="Sequence number")]

    @computed_field
    @property
    def volunteer_display_id(self) -> str:
        return f"SETN-VLR-{self.volunteer_sequence_number:04d}"


class VerifiedDTO(VolunteerDetails):
    id: Annotated[UUID, Field(description="User ID")]
    name: Annotated[str, Field(description="User name")]
    student_sequence_number: Annotated[int, Field(description="Sequence number")]
    role: Annotated[UserRole, Field(description="Role")]
    institution_name: Annotated[str, Field(description="Institution name")]
    level_of_education: Annotated[
        LevelOfEducationEnum, Field(description="Level of education")
    ]
    course: Annotated[str | None, Field(description="Courses")] = None
    semester: Annotated[int | None, Field(description="Semester")] = None
    status: Annotated[str | None, Field(description="Status")] = None

    @computed_field
    @property
    def course_or_level_of_education(self) -> str:
        if self.course:
            return self.course
        return self.level_of_education.value

    @computed_field
    @property
    def display_id(
        self,
    ) -> str:
        if self.role == UserRole.STUDENT:
            role = "USR"
        elif self.role == UserRole.VOLUNTEER:
            role = "VLR"
        else:
            role = "ADN"
        return f"SETN-{role}-{self.student_sequence_number:04d}"


class VerificationFilters(BaseCmd):
    name_or_email: Annotated[str | None, Field(description="Name")] = None
    sort_by_name: Annotated[
        Literal["asc", "desc"] | None, Field(description="Sort by name")
    ] = None
    sort_by_submitted_on: Annotated[
        Literal["asc", "desc"] | None, Field(description="Sort by submitted on")
    ] = None

    @computed_field
    @property
    def sorts(
        self,
    ) -> list[Sort]:
        list_of_sorts = []
        if self.sort_by_name:
            list_of_sorts.append(
                Sort(field="name", direction=self.sort_by_name, table="users")
            )
        if self.sort_by_submitted_on:
            list_of_sorts.append(
                Sort(
                    field="created_at",
                    direction=self.sort_by_submitted_on,
                    table="profile_verification",
                )
            )
        return list_of_sorts


class VerifiedFilters(VerificationFilters):
    status: Annotated[
        Literal["approved", "rejected"] | None, Field(description="Status")
    ] = None
    volunteer_id: Annotated[UUID | None, Field(description="Volunteer ID")] = None


class VerifiedFiltersWithPagination(PageMeta, VerifiedFilters): ...


class VerificationFiltersWithPagination(PageMeta, VerificationFilters): ...
