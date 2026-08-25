from typing import Any, ClassVar, override

from asyncpg import Connection
from asyncpg.protocol.record import Record
from pydantic import BaseModel
from pypika import Criterion, Parameter, PostgreSQLQuery, Table, functions

from src.command.commands.authentication import UpdateLastLogin
from src.command.commands.users import (
    User,
    UserCreate,
    UserGetByEmail,
    UserGetById,
    UserUpdate,
)
from src.command.repositories.base import BaseRepository
from src.database import ExecutableSQL


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

    async def update_last_login(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> User | None:
        cmd = self._normalize(cmd=cmd, model=UpdateLastLogin)

        "Updates the last login timestamp for a user in the database."

        table = Table(self.tablename)
        id = self._validate_id(getattr(cmd, "user_id", None))
        updated_id = self._validate_id(getattr(cmd, "user_id", None))

        update_query = PostgreSQLQuery.update(table).where(
            Criterion.all(
                terms=[table.id == Parameter("$1"), table.deleted_at.isnull()]
            )
        )

        values = [id]
        # Set updated_at to current timestamp
        update_query = update_query.set("updated_at", functions.Now())
        update_query = update_query.set("last_login", functions.Now())
        update_query = update_query.set("updated_by", updated_id)
        update_query: Any = update_query.returning("*")  # type: ignore
        sql: str = update_query.get_sql()

        executable = ExecutableSQL(sql=sql, values=tuple(values))

        result = await self.db.execute(executable, fetch_returns="one")

        return self._to_domain(result)

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
