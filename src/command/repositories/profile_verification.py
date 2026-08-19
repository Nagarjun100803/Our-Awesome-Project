from typing import ClassVar, override

from asyncpg import Connection
from asyncpg.protocol.record import Record
from pydantic import BaseModel

from src.command.commands.profile_verification import (
    ProfileVerification,
    ProfileVerificationCreate,
    ProfileVerificationDelete,
    ProfileVerificationGet,
    ProfileVerificationUpdate,
)
from src.command.repositories.base import BaseRepository


class ProfileVerificationRepository(BaseRepository[ProfileVerification]):
    tablename: ClassVar["str"] = "profile_verification"

    @override
    def _to_domain(self, row: Record | None) -> ProfileVerification | None:
        if row is None:
            return None
        return ProfileVerification.model_validate(dict(row))

    async def add(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> ProfileVerification:
        cmd = self._normalize(cmd=cmd, model=ProfileVerificationCreate)
        return await super().add(cmd, connection)

    async def update(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> ProfileVerification | None:
        cmd = self._normalize(cmd=cmd, model=ProfileVerificationUpdate)
        return await super().update(cmd, connection)

    async def delete(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> ProfileVerification | None:
        cmd = self._normalize(cmd=cmd, model=ProfileVerificationDelete)
        return await super().delete(cmd, connection)

    async def get(
        self, query: BaseModel, connection: Connection | None = None
    ) -> ProfileVerification | None:
        query = self._normalize(cmd=query, model=ProfileVerificationGet)
        return await super().get(query, connection)
