from datetime import datetime
from typing import ClassVar, override
from uuid import UUID

from asyncpg import Connection
from asyncpg.protocol.record import Record
from pydantic import BaseModel

from src.command.commands.personal_details import (
    GenderType,
    PersonalDetails,
    PersonalDetailsCreate,
    PersonalDetailsDelete,
    PersonalDetailsGet,
    PersonalDetailsUpdate,
)
from src.command.repositories.base import BaseRepository
from src.database import DBManager


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


async def main():
    db = DBManager()
    await db.init_pool()

    cmd = PersonalDetailsCreate(
        id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
        dob=datetime.fromisoformat("2000-01-01"),
        gender=GenderType.MALE,
        nationality="Indian",
        created_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
        phone="+91 987654321",
        alternate_phone=None,
        street="Something Street",
        city="Chennai",
        district="Chennai",
        state="Tamil Nadu",
        country="India",
        pincode="600091",
    )

    # cmd = PersonalDetailsUpdate(
    #     id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
    #     dob=datetime.fromisoformat("2000-09-15"),
    #     updated_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
    # )

    repo = PersonalDetailsRepository(db=db)

    # print(
    #     await repo.get(
    #         query=PersonalDetailsGet(id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"))
    #     )
    # )

    # print(await repo.update(cmd=cmd))
    print(await repo.add(cmd=cmd))

    await db.close_pool()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
