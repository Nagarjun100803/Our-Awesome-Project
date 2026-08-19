import asyncio
from uuid import UUID

from asyncpg import Connection

from src.command.commands.academic_details import (
    AcademicDetails,
    AcademicDetailsCreate,
    AcademicDetailsDelete,
    AcademicDetailsGet,
    AcademicDetailsGetAll,
    AcademicDetailsUpadate,
    LevelOfEducationEnum,
)
from src.command.repositories.academic_details import AcademicDetailsRepository
from src.command.services.base import BaseService
from src.database import DBManager
from src.exceptions import (
    AcademicDetailsAlreadyExistsError,
    AcademicDetailsNotFoundError,
    AcademicWithEnrollmentsNotFoundError,
)


class AcademicDetailsService(BaseService[AcademicDetails]):
    _not_found_exc = AcademicDetailsNotFoundError

    def __init__(self, repo: AcademicDetailsRepository):
        self.repo = repo

    async def create(
        self, cmd: AcademicDetailsCreate, connection: Connection | None = None
    ) -> AcademicDetails:

        if await self.repo.exists_by(
            id=cmd.id, level_of_education=cmd.level_of_education, connection=connection
        ):
            raise AcademicDetailsAlreadyExistsError(
                f"AcademicDetails Already Exists for this User-{cmd.id} with level_of_education={cmd.level_of_education}"
            )

        return self._require_entity(await self.repo.add(cmd=cmd, connection=connection))

    async def update(
        self, cmd: AcademicDetailsUpadate, connection: Connection | None = None
    ) -> AcademicDetails:

        return self._require_entity(
            await self.repo.update(cmd=cmd, connection=connection)
        )

    async def delete(
        self, cmd: AcademicDetailsDelete, connection: Connection | None = None
    ) -> AcademicDetails:

        return self._require_entity(
            await self.repo.delete(cmd=cmd, connection=connection)
        )

    async def delete_all(
        self, cmd: AcademicDetailsDelete, connection: Connection | None = None
    ) -> AcademicDetails:

        return self._require_entity(
            await self.repo.delete_all(cmd=cmd, connection=connection)
        )

    async def get(
        self, cmd: AcademicDetailsGet, connection: Connection | None = None
    ) -> AcademicDetails:
        return self._require_entity(
            await self.repo.get(query=cmd, connection=connection), id=cmd.id
        )

    async def get_all(
        self, cmd: AcademicDetailsGetAll, connection: Connection | None = None
    ) -> list[AcademicDetails]:
        records = await self.repo.get_all(query=cmd, connection=connection)

        for record in records:
            self._require_entity(record)

        return records

    async def exists_by(
        self, cmd: AcademicDetailsGetAll, connection: Connection | None = None
    ) -> bool:
        return await self.repo.exists_by(
            connection=connection, id=cmd.id, currently_enrolled=True
        )

    async def check_currently_enrolled(
        self, cmd: AcademicDetailsGetAll, connection: Connection | None = None
    ) -> bool:
        if not await self.repo.exists_by(
            connection=connection, id=cmd.id, currently_enrolled=True
        ):
            raise AcademicWithEnrollmentsNotFoundError(
                "Academic with enrollments not found"
            )

        return True


async def main():
    db = DBManager()
    await db.init_pool()

    service = AcademicDetailsService(repo=AcademicDetailsRepository(db))

    await service.delete(
        cmd=AcademicDetailsDelete(
            id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
            deleted_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
            level_of_education=LevelOfEducationEnum.SCHOOL_10TH,
        )
    )
    await db.close_pool()


if __name__ == "__main__":
    asyncio.run(main())
