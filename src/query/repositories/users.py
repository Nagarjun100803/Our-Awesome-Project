from asyncpg import Connection
from pypika import Criterion, Order, PostgreSQLQuery, Table
from pypika.queries import QueryBuilder

from src.database import DBManager, ExecutableSQL
from src.query.dto.base import PageMeta, Paginated
from src.query.dto.profile_verification import VerificationDTO
from src.query.dto.users import UserDTO, UserFilters
from src.query.repositories.mixins import PaginatorMixin


class UserReadRepository(PaginatorMixin):
    def __init__(self, db: DBManager):
        self.db = db

    def _user_query_with_filters(
        self, query: QueryBuilder, filters: UserFilters
    ) -> QueryBuilder:
        user_table = Table("users")
        if filters.name_or_email:
            query = query.where(
                Criterion.any(
                    terms=[
                        user_table.name.ilike(f"{filters.name_or_email}%"),
                        user_table.email.ilike(f"{filters.name_or_email}%"),
                    ]
                )
            )
        if filters.role:
            query = query.where(user_table.role == filters.role)
        if filters.sorts:
            for sort in filters.sorts:
                query = query.orderby(
                    Table(sort.table)[sort.field],
                    order=Order(value=sort.direction.upper()),
                )
        return query

    async def list_users(
        self,
        page_meta: PageMeta,
        filters: UserFilters,
        connection: Connection | None = None,
    ) -> Paginated[UserDTO]:
        tablename = Table("users")
        query = PostgreSQLQuery.from_(tablename).select(
            tablename.id,
            tablename.name,
            tablename.email,
            tablename.role,
            tablename.created_at,
            tablename.last_login,
            tablename.sequence_number,
        )
        # query = self._apply_user_filters(query=query, filters=filters)
        query = self._user_query_with_filters(query=query, filters=filters)

        return await self.paginate_query(
            sql=query,
            values=(),
            dto_class=UserDTO,
            page_meta=page_meta,
            connection=connection,
        )

    async def get_user_by_role(
        self,
        filters: UserFilters,
        connection: Connection | None = None,
    ):
        tablename = Table("users")
        query = PostgreSQLQuery.from_(tablename).select(
            tablename.id,
            tablename.name,
            tablename.email,
            tablename.role,
            tablename.created_at,
            tablename.last_login,
            tablename.sequence_number,
        )
        # query = self._apply_user_filters(query=query, filters=filters)
        query = self._user_query_with_filters(query=query, filters=filters)

        executable = ExecutableSQL(sql=query.get_sql(), values=())

        records = await self.db.execute(
            executable=executable, connection=connection, fetch_returns="all"
        )

        return [UserDTO.model_validate(dict(x)) for x in records]
