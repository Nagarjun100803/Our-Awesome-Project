import asyncio
from typing import Any, ClassVar, override

from asyncpg import Connection
from asyncpg.protocol.record import Record
from pydantic import BaseModel
from pypika import Criterion, Parameter, PostgreSQLQuery, Table

from src.command.commands.users import (
    User,
    UserCreate,
    UserGetByEmail,
    UserGetById,
    UserUpdate,
)
from src.command.repositories.base import BaseRepository
from src.database import DBManager, ExecutableSQL


class UserRepository(BaseRepository[User]):
    tablename: ClassVar[str] = "users"

    @override
    def _to_domain(self, row: Record | None) -> User | None:
        if not row:
            return None
        return User.model_validate(dict(row))

    async def add(self, cmd: BaseModel, connection: Connection | None = None) -> User:
        """Adds a new user to the repository."""

        cmd = self._normalize(cmd=cmd, model=UserCreate)
        return await super().add(cmd=cmd, connection=connection)

    async def update(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> User | None:
        """Updates an existing user in the repository."""

        cmd = self._normalize(cmd=cmd, model=UserUpdate)
        return await super().update(cmd=cmd, connection=connection)

    async def delete(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> None:
        """Deletes a user from the repository."""

    async def get(
        self, query: BaseModel, connection: Connection | None = None
    ) -> User | None:
        """Gets a user from the repository by ID."""

        query = self._normalize_one_of(cmd=query, models=[UserGetById, UserGetByEmail])

        if isinstance(query, UserGetById):
            return await super().get(query, connection)

        table = Table(self.tablename)
        sql = (
            PostgreSQLQuery.from_(table)
            .select("*")
            .where(
                Criterion.all(
                    terms=[table.email == Parameter("$1"), table.deleted_at.isnull()]
                )
            )
        )
        executable = ExecutableSQL(sql=sql.get_sql(), values=(query.email,))

        user = await self.db.execute(
            executable,
            fetch_returns="one",
            connection=connection,
        )

        return self._to_domain(user)

    async def exists_by(
        self, connection: Connection | None = None, **filters: Any
    ) -> bool:
        """Checks if a user exists in the repository by the given filters."""

        return await super().exists_by(connection, **filters)


async def main():

    db = DBManager()
    await db.init_pool()

    repo = UserRepository(db=db)
    # user = await repo.add(
    #     UserCreate(name="praveen", email="234asdf11123@gmail.com", password=None), None
    # )

    user = await repo.pick(
        columns=["id", "name", "email"],
        fetch_all=False,
        connection=None,
        name="ARUL",
    )

    # user_update = await repo.update(
    #     UserUpdate(
    #         id=UUID("06acb0eb-94cd-42ba-9c82-99319954be78"),
    #         password="23421",
    #         updated_by=UUID("06acb0eb-94cd-42ba-9c82-99319954be78"),
    #     ),
    #     None,
    # )

    # exists = await repo.exists_by(
    #     email="234adf11123@gmail.com", id=UUID("06acb0eb-94cd-42ba-9c82-99319954be78")
    # )

    # user = await repo.get(
    #     query=UserGetById(id=UUID("06acb0eb-94cd-42ba-9c82-99319954be78"))
    # )
    await db.close_pool()
    print(user)

    # print("---update----", user_update)

    # print("----exists---", exists)


if __name__ == "__main__":
    asyncio.run(main())
