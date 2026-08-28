from typing import ClassVar

from asyncpg import Connection

from src.command.commands.personal_details import (
    PersonalDetails,
    PersonalDetailsCreate,
    PersonalDetailsDelete,
    PersonalDetailsGet,
    PersonalDetailsUpdate,
)
from src.command.repositories.personal_details import PersonalDetailsRepository
from src.command.services.base import BaseService
from src.exceptions import (
    NotFoundException,
    PersonalDetailsAlreadyExistsError,
    PersonalDetailsNotFoundError,
)


class PersonalDetailsService(BaseService[PersonalDetails]):
    _not_found_exc: ClassVar[type[NotFoundException]] = PersonalDetailsNotFoundError

    def __init__(self, repo: PersonalDetailsRepository):
        self.repo: PersonalDetailsRepository = repo

    async def create(
        self, cmd: PersonalDetailsCreate, connection: Connection | None = None
    ) -> PersonalDetails:

        if await self.repo.exists_by(id=cmd.id):
            raise PersonalDetailsAlreadyExistsError(
                f"PersonalDetails Already Exists for this User-{cmd.id}"
            )

        return self._require_entity(await self.repo.add(cmd=cmd, connection=connection))

    async def update(
        self, cmd: PersonalDetailsUpdate, connection: Connection | None = None
    ) -> PersonalDetails:

        return self._require_entity(
            await self.repo.update(cmd=cmd, connection=connection)
        )

    async def delete(
        self, cmd: PersonalDetailsDelete, connection: Connection | None = None
    ) -> PersonalDetails:

        return self._require_entity(
            await self.repo.delete(cmd=cmd, connection=connection)
        )

    async def get(
        self, cmd: PersonalDetailsGet, connection: Connection | None = None
    ) -> PersonalDetails:
        return self._require_entity(
            await self.repo.get(query=cmd, connection=connection)
        )

    async def exists_by(
        self, cmd: PersonalDetailsGet, connection: Connection | None = None
    ) -> bool:
        return await self.repo.exists_by(connection=connection, id=cmd.id)
