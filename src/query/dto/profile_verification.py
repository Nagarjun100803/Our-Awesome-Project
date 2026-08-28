from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, computed_field

from src.command.commands.academic_details import LevelOfEducationEnum
from src.command.commands.base import BaseCmd
from src.command.commands.users import UserRole

# from src.core.storage.s3 import FileMetadata
# from src.dependencies import s3_bucket
from src.query.dto.base import PageMeta, Sort


class VerificationDTO(BaseCmd):
    id: Annotated[UUID, Field(description="User ID")]
    name: Annotated[str, Field(description="User name")]
    student_sequence_number: Annotated[
        int, Field(description="Sequence number", exclude=True)
    ]
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
        return f"SETN-{role}-{self.student_sequence_number:04d}"


class VolunteerDetails(BaseCmd):
    volunteer_id: Annotated[UUID | None, Field(description="User ID")] = None
    volunteer_name: Annotated[str | None, Field(description="User name")] = None
    volunteer_sequence_number: Annotated[
        int | None, Field(description="Sequence number")
    ] = None
    volunteer_role: Annotated[UserRole, Field(description="Role")]

    @computed_field
    @property
    def volunteer_display_id(self) -> str | None:
        if not self.volunteer_sequence_number:
            return None
        if self.volunteer_role == UserRole.VOLUNTEER:
            return f"SETN-VLR-{self.volunteer_sequence_number:04d}"
        else:
            return f"SETN-ADN-{self.volunteer_sequence_number:04d}"


class VerifiedDTO(VolunteerDetails):
    id: Annotated[UUID, Field(description="User ID")]
    name: Annotated[str, Field(description="User name")]
    student_sequence_number: Annotated[
        int, Field(description="Sequence number", exclude=True)
    ]
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


class ProfileData(BaseCmd):
    name: Annotated[str, Field(description="User name")]
    dob: Annotated[datetime, Field(description="Date of Birth")]
    document_type: Annotated[str, Field(description="Document Type ")] = (
        "College ID Card"
    )
    contact_number: Annotated[str, Field(description="User Phone Number")]
    address: Annotated[str, Field(description="Address", exclude=True)]
    city: Annotated[str, Field(description="City", exclude=True)]
    district: Annotated[str, Field(description="District", exclude=True)]
    state: Annotated[str, Field(description="State", exclude=True)]
    pincode: Annotated[str, Field(description="pincode", exclude=True)]

    @computed_field
    @property
    def location(self) -> str:
        return f"{self.address}, {self.city} - {self.pincode}, {self.district} district, {self.state}"


class EducationDetails(BaseCmd):
    current_education_level: Annotated[
        str, Field(description="current educational level of the user")
    ]
    course_stream_specialization: Annotated[
        str | None, Field(description="course_stream_specialization")
    ] = None
    institution_name: Annotated[str, Field(description="Name of the Institution")]
    register_number: Annotated[
        str | None, Field(description="Register Number of the user")
    ] = None
    current_semester: Annotated[int | None, Field(description="current semester")] = (
        None
    )
    year_of_passing: Annotated[str, Field(description="year of passing")]


class MediaDetails(BaseCmd):
    # filename: Annotated[str, Field(description="file name", exclude=True)]
    # content_type: Annotated[
    #     str, Field(description="content type of the file", exclude=True)
    # ]
    # storage_key: Annotated[str, Field(description="storage key", exclude=True)]

    filename: Annotated[str, Field(description="file name")]
    content_type: Annotated[str, Field(description="content type of the file")]
    storage_key: Annotated[str, Field(description="storage key")]
    # media_url: Annotated[str, Field(description="Url of the file")]

    # @computed_field
    # @property
    # async def media_url(self) -> str:
    #     return await s3_bucket.get_view_url(
    #         metadata=FileMetadata(self.storage_key, self.filename, self.content_type)
    #     )


class GetParticular(ProfileData, EducationDetails, MediaDetails):
    status: Annotated[
        str | None,
        Field(
            description="status of the verification - Approved or rejected or pending"
        ),
    ]


class GetVerifiedParticular(GetParticular, VolunteerDetails):
    status: Annotated[
        str | None,
        Field(
            description="status of the verification - Approved or rejected or pending"
        ),
    ] = None


class GetParticularRecordResponse(BaseCmd):
    name: Annotated[str, Field(description="User name")]
    dob: Annotated[datetime, Field(description="Date of Birth")]
    document_type: Annotated[str, Field(description="Document Type ")] = (
        "College ID Card"
    )
    contact_number: Annotated[str, Field(description="User Phone Number")]
    location: Annotated[str, Field(description="Location")]

    current_education_level: Annotated[
        str, Field(description="current educational level of the user")
    ]
    course_stream_specialization: Annotated[
        str | None, Field(description="course_stream_specialization")
    ] = None
    institution_name: Annotated[str, Field(description="Name of the Institution")]
    register_number: Annotated[
        str | None, Field(description="Register Number of the user")
    ] = None
    current_semester: Annotated[int | None, Field(description="current semester")] = (
        None
    )
    year_of_passing: Annotated[str, Field(description="year of passing")]

    status: Annotated[
        str | None,
        Field(
            description="status of the verification - Approved or rejected or pending"
        ),
    ]

    # volunteer_id: Annotated[UUID | None, Field(description="User ID")] = None
    # volunteer_name: Annotated[str | None, Field(description="User name")] = None
    # volunteer_display_id: Annotated[str | None, Field(description="User name")] = None

    media_url: Annotated[str, Field(description="media url")]


class GetVerifiedParticularResponse(GetParticularRecordResponse):
    volunteer_id: Annotated[UUID | None, Field(description="User ID")] = None
    volunteer_name: Annotated[str | None, Field(description="User name")] = None
    volunteer_display_id: Annotated[str | None, Field(description="User name")] = None


class VerifiedFiltersWithPagination(PageMeta, VerifiedFilters): ...


class VerificationFiltersWithPagination(PageMeta, VerificationFilters): ...
