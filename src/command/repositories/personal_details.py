from typing import ClassVar, override

from asyncpg import Connection
from asyncpg.protocol.record import Record
from pydantic import BaseModel

from src.command.commands.personal_details import (
    PersonalDetails,
    PersonalDetailsCreate,
    PersonalDetailsDelete,
    PersonalDetailsGet,
    PersonalDetailsUpdate,
)
from src.command.repositories.base import BaseRepository


class PersonalDetailsRepository(BaseRepository[PersonalDetails]):
    tablename: ClassVar[str] = "personal_details"

    @override
    def _to_domain(self, row: Record | None) -> PersonalDetails | None:
        if row is None:
            return None
        return PersonalDetails.model_validate(dict(row))

    async def add(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> PersonalDetails:
        cmd = self._normalize(cmd=cmd, model=PersonalDetailsCreate)
        return await super().add(cmd, connection)

    async def update(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> PersonalDetails | None:
        cmd = self._normalize(cmd=cmd, model=PersonalDetailsUpdate)
        return await super().update(cmd, connection)

    async def get(
        self, query: BaseModel, connection: Connection | None = None
    ) -> PersonalDetails | None:
        query = self._normalize(cmd=query, model=PersonalDetailsGet)

        return await super().get(query, connection)

    async def delete(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> PersonalDetails | None:
        cmd = self._normalize(cmd=cmd, model=PersonalDetailsDelete)
        return await super().delete(cmd, connection)
