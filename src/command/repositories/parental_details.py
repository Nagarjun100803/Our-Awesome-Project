from typing import ClassVar, override
from uuid import UUID

from asyncpg import Connection
from asyncpg.protocol import Record
from pydantic import BaseModel

from src.command.commands.parental_details import (
    AnnualFamilyIncomeEnum,
    OccupationEnum,
    ParentalDetails,
    ParentalDetailsCreate,
    ParentalDetailsDelete,
    ParentalDetailsGet,
    ParentalDetailsUpdate,
)
from src.command.repositories.base import BaseRepository
from src.database import DBManager


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


async def main():
    db = DBManager()
    await db.init_pool()

    repo = ParentalDetailsRepository(db)

    cmd = ParentalDetailsCreate(
        id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
        father_name="Sampath",
        father_occupation=OccupationEnum.OTHER,
        father_mobile="+916391733560",
        annual_family_income=AnnualFamilyIncomeEnum.BELOW_100K,
        created_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
    )

    result = await repo.add(cmd)
    print(result)

    await db.close_pool()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
