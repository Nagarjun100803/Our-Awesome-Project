import asyncio
from uuid import UUID

from src.command.commands.academic_details import (
    AcademicDetails,
    AcademicDetailsCreate,
    AcademicDetailsDelete,
    AcademicDetailsGetAll,
    AcademicDetailsUpadate,
)
from src.command.commands.parental_details import (
    ParentalDetails,
    ParentalDetailsCreate,
    ParentalDetailsGet,
)
from src.command.commands.personal_details import (
    PersonalDetails,
    PersonalDetailsCreate,
    PersonalDetailsGet,
)
from src.command.repositories.academic_details import AcademicDetailsRepository
from src.command.repositories.parental_details import ParentalDetailsRepository
from src.command.repositories.personal_details import PersonalDetailsRepository
from src.command.services.academic_details import AcademicDetailsService
from src.command.services.parental_details import ParentalDetailsService
from src.command.services.personal_details import PersonalDetailsService
from src.database import DBManager
from src.exceptions import (
    AcademicDetailsNotUnique,
    AcademicWithEnrollmentsNotFoundError,
)


class ProfileCompletionService:
    def __init__(
        self,
        personal_service: PersonalDetailsService,
        parental_service: ParentalDetailsService,
        academic_service: AcademicDetailsService,
    ) -> None:
        self.personal_service = personal_service
        self.parental_service = parental_service
        self.academic_service = academic_service

    async def save_personal(self, cmd: PersonalDetailsCreate) -> PersonalDetails:
        return await self.personal_service.create(cmd)

    async def save_parental(self, cmd: ParentalDetailsCreate) -> ParentalDetails:
        return await self.parental_service.create(cmd)

    async def save_academic(self, cmd: AcademicDetailsCreate) -> AcademicDetails:
        return await self.academic_service.create(cmd)

    async def get_academic(self, cmd: AcademicDetailsGetAll) -> list[AcademicDetails]:
        return await self.academic_service.get_all(cmd)

    async def update_academic(self, cmd: AcademicDetailsUpadate) -> AcademicDetails:
        return await self.academic_service.update(cmd)

    async def delete_academic(self, cmd: AcademicDetailsDelete) -> AcademicDetails:
        return await self.academic_service.delete(cmd)

    async def academic_next(self, id: UUID) -> None:
        if not await self.academic_service.exists_by(cmd=AcademicDetailsGetAll(id=id)):
            raise AcademicWithEnrollmentsNotFoundError()

    async def is_completed(self, id: UUID):
        """
        If i get the userId then i will find is they complete or not
        """
        records = await asyncio.gather(
            self.personal_service.exists_by(cmd=PersonalDetailsGet(id=id)),
            self.academic_service.exists_by(cmd=AcademicDetailsGetAll(id=id)),
            self.parental_service.exists_by(cmd=ParentalDetailsGet(id=id)),
        )

        return records  # [true, true, true]


async def main():
    db = DBManager()
    await db.init_pool()

    profile_completion_service = ProfileCompletionService(
        personal_service=PersonalDetailsService(repo=PersonalDetailsRepository(db=db)),
        academic_service=AcademicDetailsService(repo=AcademicDetailsRepository(db=db)),
        parental_service=ParentalDetailsService(repo=ParentalDetailsRepository(db=db)),
    )

    print(
        await profile_completion_service.is_completed(
            id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850")
        )
    )

    await db.close_pool()


if __name__ == "__main__":
    asyncio.run(main())
