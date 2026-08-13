import asyncio
from typing import Any
from uuid import UUID

from src.command.commands.academic_details import (
    AcademicDetails,
    AcademicDetailsCreate,
    LevelOfEducationEnum,
)
from src.command.commands.parental_details import ParentalDetails, ParentalDetailsCreate
from src.command.commands.personal_details import PersonalDetails, PersonalDetailsCreate
from src.command.repositories.academic_details import AcademicDetailsRepository
from src.command.repositories.parental_details import ParentalDetailsRepository
from src.command.repositories.personal_details import PersonalDetailsRepository
from src.database import DBManager


class CompleteProfile:
    def __init__(
        self,
        personal_details_repo: PersonalDetailsRepository,
        parental_details_repo: ParentalDetailsRepository,
        academic_details_repo: AcademicDetailsRepository,
    ):
        self.personal_details_repo = personal_details_repo
        self.parental_details_repo = parental_details_repo
        self.academic_details_repo = academic_details_repo

    def _require_entity(
        self,
        record: PersonalDetails | ParentalDetails | AcademicDetails | None,
        **kwargs: Any,
    ) -> PersonalDetails | ParentalDetails | AcademicDetails:
        """Raises a ValueError if the record is None.
        Used to ensure a record exists before returning it while fetching from the repository."""

        if not record:
            raise ValueError("Record not found")
        return record

    async def save_personal_details(
        self, cmd: PersonalDetailsCreate
    ) -> PersonalDetails:
        return await self.personal_details_repo.add(cmd)

    async def save_parental_details(
        self, cmd: ParentalDetailsCreate
    ) -> ParentalDetails:
        return await self.parental_details_repo.add(cmd)

    async def save_academic_details(
        self, cmd: list[AcademicDetailsCreate]
    ) -> list[AcademicDetails]:
        have_enrolled = False
        for x in cmd:
            if x.currently_enrolled:
                have_enrolled = True

        if not have_enrolled:
            raise ValueError("No enrolled academic details found")

        return await asyncio.gather(*[self._save_academic(x) for x in cmd])

    async def _save_academic(self, cmd: AcademicDetailsCreate) -> AcademicDetails:
        if await self.academic_details_repo.exists_by(
            id=cmd.id, level_of_education=cmd.level_of_education
        ):
            raise ValueError(
                f"Academic details already exist with user id={cmd.id} and level_of_education={cmd.level_of_education}"
            )
        return await self.academic_details_repo.add(cmd)


async def main():
    db = DBManager()
    await db.init_pool()

    personal_details_repo = PersonalDetailsRepository(db)
    parental_details_repo = ParentalDetailsRepository(db)
    academic_details_repo = AcademicDetailsRepository(db)

    profile_service = CompleteProfile(
        personal_details_repo=personal_details_repo,
        parental_details_repo=parental_details_repo,
        academic_details_repo=academic_details_repo,
    )

    cmd = AcademicDetailsCreate(
        id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
        created_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
        level_of_education=LevelOfEducationEnum.UNDERGRADUATE,
        institution_name="University College of Engineering Tindivanam",
        board_university="Anna University",
        course_stream_specialization="B.Tech Information Technology",
        year_of_passing="2026",
    )

    cmd2 = AcademicDetailsCreate(
        id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
        created_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
        level_of_education=LevelOfEducationEnum.UNDERGRADUATE,
        institution_name="University College of Engineering Tindivanam",
        board_university="Anna University",
        course_stream_specialization="B.Tech Information Technology",
        year_of_passing="2026",
        currently_enrolled=True,
    )
    await profile_service.save_academic_details([cmd, cmd2])

    await db.close_pool()


if __name__ == "__main__":
    asyncio.run(main())
