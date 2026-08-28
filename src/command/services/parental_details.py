from typing import ClassVar

from asyncpg import Connection

from src.command.commands.parental_details import (
    ParentalDetails,
    ParentalDetailsCreate,
    ParentalDetailsDelete,
    ParentalDetailsGet,
    ParentalDetailsUpdate,
)
from src.command.repositories.parental_details import ParentalDetailsRepository
from src.command.services.base import BaseService
from src.exceptions import (
    NotFoundException,
    ParentalDetailsAlreadyExistsError,
    ParentalDetailsNotFoundError,
)


class ParentalDetailsService(BaseService[ParentalDetails]):
    _not_found_exc: ClassVar[type[NotFoundException]] = ParentalDetailsNotFoundError

    def __init__(self, repo: ParentalDetailsRepository):
        self.repo: ParentalDetailsRepository = repo

    async def create(
        self, cmd: ParentalDetailsCreate, connection: Connection | None = None
    ) -> ParentalDetails:

        if await self.repo.exists_by(id=cmd.id):
            raise ParentalDetailsAlreadyExistsError(
                f"ParentalDetails Already Exists for this User-{cmd.id}"
            )

        return self._require_entity(await self.repo.add(cmd, connection))

    async def update(
        self, cmd: ParentalDetailsUpdate, connection: Connection | None = None
    ) -> ParentalDetails:

        return self._require_entity(await self.repo.update(cmd, connection))

    async def delete(
        self, cmd: ParentalDetailsDelete, connection: Connection | None = None
    ) -> ParentalDetails:

        return self._require_entity(await self.repo.delete(cmd, connection))

    async def get(
        self, cmd: ParentalDetailsGet, connection: Connection | None = None
    ) -> ParentalDetails:
        return self._require_entity(
            await self.repo.get(query=cmd, connection=connection)
        )

    async def exists_by(
        self, cmd: ParentalDetailsGet, connection: Connection | None = None
    ) -> bool:
        return await self.repo.exists_by(connection=connection, id=cmd.id)
