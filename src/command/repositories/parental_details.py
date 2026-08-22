from typing import ClassVar, override

from asyncpg import Connection
from asyncpg.protocol.record import Record
from pydantic import BaseModel

from src.command.commands.parental_details import (
    ParentalDetails,
    ParentalDetailsCreate,
    ParentalDetailsDelete,
    ParentalDetailsGet,
    ParentalDetailsUpdate,
)
from src.command.repositories.base import BaseRepository


class ParentalDetailsRepository(BaseRepository[ParentalDetails]):
    tablename: ClassVar[str] = "parental_details"

    @override
    def _to_domain(self, row: Record | None) -> ParentalDetails | None:
        if row is None:
            return None
        return ParentalDetails.model_validate(dict(row))

    async def add(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> ParentalDetails:
        cmd = self._normalize(cmd=cmd, model=ParentalDetailsCreate)
        return await super().add(cmd, connection)

    async def update(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> ParentalDetails | None:
        cmd = self._normalize(cmd=cmd, model=ParentalDetailsUpdate)
        return await super().update(cmd, connection)

    async def get(
        self, query: BaseModel, connection: Connection | None = None
    ) -> ParentalDetails | None:
        query = self._normalize(cmd=query, model=ParentalDetailsGet)
        return await super().get(query, connection)

    async def delete(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> ParentalDetails | None:
        cmd = self._normalize(cmd=cmd, model=ParentalDetailsDelete)
        return await super().delete(cmd, connection)
