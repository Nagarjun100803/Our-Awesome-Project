from pypika import Criterion, PostgreSQLQuery, Table

from src.command.commands.college_lookup import CollegeLookup, CollegeLookupGet
from src.database import DBManager, ExecutableSQL


class CollegeLookupRepository:
    def __init__(self, db):
        self.db = db

    tablename = "colleges"

    async def get(self, query: CollegeLookupGet) -> list[CollegeLookup]:
        """
        Retrieves a list of colleges from the database.
        """

        name = query.name

        table = Table(self.tablename)
        sql = (
            PostgreSQLQuery.from_(table)
            .select("*")
            .where(
                Criterion.any(
                    terms=[
                        table.name.ilike(f"%{name}%"),
                    ]
                )
            )
        )

        executable = ExecutableSQL(sql=sql.get_sql(), values=())

        records = await self.db.execute(executable, fetch_returns="all")
        print("records", records)
        list_of_colleges = []
        for record in records:
            list_of_colleges.append(CollegeLookup.model_validate(dict(record)))

        print("Repo", list_of_colleges)

        return list_of_colleges


async def main():
    db = DBManager()
    await db.init_pool()

    repo = CollegeLookupRepository(db)

    result = await repo.get(CollegeLookupGet(name="tindivanam"))
    print(result)
    await db.close_pool()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
