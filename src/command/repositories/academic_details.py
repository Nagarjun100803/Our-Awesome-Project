from typing import Any, ClassVar, cast, override
from uuid import UUID

from asyncpg import Connection
from asyncpg.protocol.record import Record
from pydantic import BaseModel
from pypika import Criterion, Parameter, PostgreSQLQuery, Table, functions

from src.command.commands.academic_details import (
    AcademicDetails,
    AcademicDetailsCreate,
    AcademicDetailsDelete,
    AcademicDetailsDeleteAll,
    AcademicDetailsGet,
    AcademicDetailsGetAll,
    AcademicDetailsUpadate,
)
from src.command.repositories.base import BaseRepository
from src.database import DBManager, ExecutableSQL


class AcademicDetailsRepository(BaseRepository[AcademicDetails]):
    tablename: ClassVar[str] = "academic_details"

    @override
    def _to_domain(self, row: Record | None) -> AcademicDetails | None:
        if row is None:
            return None
        return AcademicDetails.model_validate(dict(row))

    async def add(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> AcademicDetails:
        cmd = self._normalize(cmd=cmd, model=AcademicDetailsCreate)
        return await super().add(cmd, connection)

    async def update(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> AcademicDetails | None:
        cmd = self._normalize(cmd=cmd, model=AcademicDetailsUpadate)

        table = Table(self.tablename)
        id = self._validate_id(cmd.id)
        updated_id = self._validate_id(cmd.updated_by)
        level_of_education = cmd.level_of_education

        data_dict = cmd.model_dump(exclude={"id", "updated_by"}, exclude_none=True)
        update_query = PostgreSQLQuery.update(table).where(
            Criterion.all(
                terms=[
                    table.id == Parameter("$1"),
                    table.level_of_education == Parameter("$2"),
                    table.deleted_at.isnull(),
                ]
            )
        )

        values = [id, level_of_education]
        for idx, col in enumerate(data_dict.keys(), start=3):
            update_query = update_query.set(col, Parameter(f"${idx}"))
            value = data_dict[col]
            values.append(value)

        # Set updated_at to current timestamp
        update_query = update_query.set("updated_at", functions.Now())
        update_query = update_query.set("updated_by", updated_id)
        update_query: Any = update_query.returning("*")  # type: ignore
        sql: str = update_query.get_sql()

        executable = ExecutableSQL(sql=sql, values=tuple(values))

        result = await self.db.execute(executable, fetch_returns="one")

        return self._to_domain(result)

    async def get_all(
        self, query: BaseModel, connection: Connection | None = None
    ) -> list[AcademicDetails]:
        query = self._normalize(cmd=query, model=AcademicDetailsGetAll)

        id = self._validate_id(query.id)

        table = Table(self.tablename)
        sql = (
            PostgreSQLQuery.from_(table)
            .select("*")
            .where(
                Criterion.all(
                    terms=[table.id == Parameter("$1"), table.deleted_at.isnull()]
                )
            )
        )

        executable = ExecutableSQL(sql=sql.get_sql(), values=(id,))

        result = await self.db.execute(executable, fetch_returns="all")

        # list_of_record = []
        # for x in result:
        #     x = self._to_domain(x)
        #     list_of_record.append(x)

        return [cast(AcademicDetails, self._to_domain(x)) for x in result]

    async def get(
        self, query: BaseModel, connection: Connection | None = None
    ) -> AcademicDetails | None:
        query = self._normalize(cmd=query, model=AcademicDetailsGet)
        id = self._validate_id(query.id)
        level_of_education = query.level_of_education

        table = Table(self.tablename)
        sql = (
            PostgreSQLQuery.from_(table)
            .select("*")
            .where(
                Criterion.all(
                    terms=[
                        table.id == Parameter("$1"),
                        table.level_of_education == Parameter("$2"),
                        table.deleted_at.isnull(),
                    ]
                )
            )
        )

        executable = ExecutableSQL(sql=sql.get_sql(), values=(id, level_of_education))

        result = await self.db.execute(executable, fetch_returns="one")

        return self._to_domain(result)

    async def delete(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> AcademicDetails | None:
        cmd = self._normalize(cmd=cmd, model=AcademicDetailsDelete)

        table = Table(self.tablename)

        id = self._validate_id(cmd.id)
        deleted_by = self._validate_id(cmd.deleted_by)
        level_of_education = cmd.level_of_education

        delete_query = (
            PostgreSQLQuery.update(table)
            .set("deleted_at", functions.Now())
            .set("deleted_by", deleted_by)
            .where(
                Criterion.all(
                    terms=[
                        table.id == Parameter("$1"),
                        table.level_of_education == Parameter("$2"),
                        table.deleted_at.isnull(),
                    ]
                )
            )
        )
        delete_query: Any = delete_query.returning("*")
        sql: str = delete_query.get_sql()
        executable = ExecutableSQL(sql=sql, values=(id, level_of_education))

        result = await self.db.execute(executable, fetch_returns="one")

        return self._to_domain(result)

    async def delete_all(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> AcademicDetails | None:
        cmd = self._normalize(cmd, model=AcademicDetailsDeleteAll)
        return await super().delete(cmd, connection)


async def main():
    db = DBManager()
    await db.init_pool()

    # cmd = AcademicDetailsCreate(
    #     id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
    #     created_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
    #     level_of_education=LevelOfEducationEnum.UNDERGRADUATE,
    #     institution_name="University College of Engineering Tindivanam",
    #     board_university="Anna University",
    #     course_stream_specialization="B.Tech Information Technology",
    #     year_of_passing="2026",
    # )

    repo = AcademicDetailsRepository(db=db)

    # cmd = AcademicDetailsCreate(
    #     id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
    #     created_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
    #     level_of_education=LevelOfEducationEnum.SCHOOL_10TH,
    #     institution_name="Indo American Matric Hr. Sec School Cheyyar",
    #     board_university="Tamil Nadu State Board",
    #     year_of_passing="2019",
    # )

    # print(await repo.add(cmd=cmd))

    # query = AcademicDetailsDelete(
    #     id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
    #     deleted_by=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"),
    # )
    #
    # query = AcademicDetailsGet(id=UUID("522cc2cf-e3e8-46f3-9457-0d3dbddaa850"))
    # print(await repo.get_all(query=query))

    await db.close_pool()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
