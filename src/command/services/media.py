from asyncpg import Connection

from src.command.commands.media import (
    Media,
    MediaCreate,
    MediaDelete,
    MediaGet,
    MediaUpdate,
)
from src.command.repositories.media import MediaRepository
from src.command.services.base import BaseService
from src.exceptions import MediaNotFoundError


class MediaService(BaseService[Media]):
    _not_found_exc = MediaNotFoundError

    def __init__(self, repo: MediaRepository):
        self.repo = repo

    async def create(
        self, cmd: MediaCreate, connection: Connection | None = None
    ) -> Media:
        return await self.repo.add(cmd=cmd, connection=connection)

    async def get(self, cmd: MediaGet, connection: Connection | None = None) -> Media:
        return self._require_entity(
            await self.repo.get(query=cmd, connection=connection)
        )

    async def delete(
        self, cmd: MediaDelete, connection: Connection | None = None
    ) -> Media:
        return self._require_entity(
            await self.repo.delete(cmd=cmd, connection=connection)
        )

    async def update(
        self, cmd: MediaUpdate, connection: Connection | None = None
    ) -> Media:
        return self._require_entity(
            await self.repo.update(cmd=cmd, connection=connection)
        )
