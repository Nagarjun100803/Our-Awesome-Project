from typing import ClassVar, override

from asyncpg import Connection
from asyncpg.protocol.record import Record
from pydantic import BaseModel
from pypika import Criterion, Parameter, PostgreSQLQuery, Table, functions

from src.command.commands.providers import (
    Provider,
    ProviderCreate,
    ProviderDelete,
    ProviderGet,
)
from src.command.repositories.base import BaseRepository
from src.database import ExecutableSQL


class ProviderRepository(BaseRepository[Provider]):
    tablename: ClassVar[str] = "providers"

    @override
    def _to_domain(self, row: Record | None) -> Provider | None:
        if not row:
            return None
        return Provider.model_validate(dict(row))

    async def add(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> Provider:
        """
        Adds a new provider to the database.
        """
        cmd = self._normalize(cmd=cmd, model=ProviderCreate)
        return await super().add(cmd, connection)

    async def update(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> Provider | None: ...

    async def get(
        self, query: BaseModel, connection: Connection | None = None
    ) -> Provider | None:
        """
        Retrieves a provider from the database based on the given query.
        """
        query = self._normalize(cmd=query, model=ProviderGet)

        table = Table(self.tablename)
        sql = (
            PostgreSQLQuery.from_(table)
            .select("*")
            .where(
                Criterion.all(
                    terms=[
                        table.user_id == Parameter("$1"),
                        table.name == Parameter("$2"),
                        table.deleted_at.isnull(),
                    ]
                )
            )
        )
        executable = ExecutableSQL(
            sql=sql.get_sql(), values=(query.user_id, query.name)
        )

        user = await self.db.execute(
            executable,
            fetch_returns="one",
            connection=connection,
        )

        return self._to_domain(user)

    async def delete(
        self, cmd: BaseModel, connection: Connection | None = None
    ) -> None:
        """
        soft Deletes a provider from the database based on the given query.
        """
        cmd = self._normalize(cmd=cmd, model=ProviderDelete)

        table = Table(self.tablename)

        sql = (
            PostgreSQLQuery.from_(table)
            .set("deleted_at", functions.Now())
            .where(
                Criterion.all(
                    terms=[
                        table.user_id == Parameter("$1"),
                        table.name == Parameter("$2"),
                    ]
                )
            )
        )
        executable = ExecutableSQL(sql=sql.get_sql(), values=(cmd.user_id, cmd.name))
        await self.db.execute(
            executable,
            fetch_returns="none",
            connection=connection,
        )
