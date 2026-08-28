from typing import ClassVar, override

from asyncpg import Connection
from asyncpg.protocol.record import Record
from pydantic import BaseModel

from src.command.commands.media import (
    Media,
    MediaCreate,
    MediaDelete,
    MediaGet,
    MediaUpdate,
)
from src.command.repositories.base import BaseRepository


class MediaRepository(BaseRepository[Media]):
    tablename: ClassVar[str] = "media"

    @override
    def _to_domain(self, row: Record | None) -> Media | None:
        if row is None:
            return None
        return Media.model_validate(dict(row))

    async def add(self, cmd: BaseModel, connection: Connection | None = None) -> Media:
        cmd = self._normalize(cmd=cmd, model=MediaCreate)
        return await super().add(cmd, connection)

    async def update(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> Media | None:
        cmd = self._normalize(cmd=cmd, model=MediaUpdate)
        return await super().update(cmd, connection)

    async def get(
        self, query: BaseModel, connection: Connection | None = None
    ) -> Media | None:

        query = self._normalize(cmd=query, model=MediaGet)
        return await super().get(query, connection)

    async def delete(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> Media | None:
        cmd = self._normalize(cmd=cmd, model=MediaDelete)
        return await super().delete(cmd, connection)
