from asyncpg import Connection
from pypika import Criterion, PostgreSQLQuery, Table
from pypika.enums import Order
from pypika.queries import QueryBuilder

from src.database import DBManager
from src.query.dto.base import PageMeta, Paginated
from src.query.dto.profile_verification import (
    VerificationDTO,
    VerificationFilters,
    VerifiedDTO,
    VerifiedFilters,
)
from src.query.repositories.mixins import PaginatorMixin


class VerificationReadRepository(PaginatorMixin):
    def __init__(self, db: DBManager):
        self.db = db

    def _query_with_filters(
        self,
        query: QueryBuilder,
        filters: VerificationFilters | VerifiedFilters,
    ) -> QueryBuilder:

        user_table = Table("users")
        profile_table = Table("profile_verification")

        if filters.name_or_email:
            query = query.where(
                Criterion.any(
                    terms=[
                        user_table.name.like(f"%{filters.name_or_email}%"),
                        user_table.email.like(f"%{filters.name_or_email}%"),
                    ]
                )
            )

        if filters.sorts:
            for sort in filters.sorts:
                query = query.orderby(
                    Table(sort.table)[sort.field],
                    order=Order(value=sort.direction.upper()),
                )

        if isinstance(filters, VerifiedFilters):
            if filters.status:
                query = query.where(profile_table.status == filters.status)
            if filters.volunteer_id:
                query = query.where(profile_table.updated_by == filters.volunteer_id)

        return query

    async def pending_verification(
        self,
        filters: VerificationFilters,
        page_meta: PageMeta,
        connection: Connection | None = None,
    ) -> Paginated[VerificationDTO]:
        profile_table = Table("profile_verification")
        academic_table = Table("academic_details")
        user_table = Table("users")

        query = (
            PostgreSQLQuery.from_(profile_table)
            .where(
                Criterion.all(
                    terms=[
                        profile_table.deleted_at.isnull(),
                        profile_table.status == "pending",
                    ]
                )
            )
            .join(academic_table)
            .on(profile_table.id == academic_table.id)
            .where(
                Criterion.all(
                    terms=[
                        academic_table.currently_enrolled == True,
                        academic_table.deleted_at.isnull(),
                    ]
                )
            )
            .join(user_table)
            .on(academic_table.id == user_table.id)
            .where(user_table.deleted_at.isnull())
            .select(
                user_table.id.as_("id"),
                user_table.name.as_("name"),
                user_table.sequence_number.as_("sequence_number"),
                user_table.role.as_("role"),
                academic_table.institution_name.as_("institution_name"),
                academic_table.course_stream_specialization.as_("course"),
                academic_table.level_of_education.as_("level_of_education"),
                academic_table.current_semester.as_("semester"),
                profile_table.created_at.as_("submitted_on"),
            )
        )
        query = self._query_with_filters(query, filters)

        return await self.paginate_query(
            sql=query,
            values=(),
            dto_class=VerificationDTO,
            page_meta=page_meta,
            connection=connection,
        )

    async def verified_entries(
        self,
        filters: VerifiedFilters,
        page_meta: PageMeta,
        connection: Connection | None = None,
    ) -> Paginated[VerifiedDTO]:
        profile_table = Table("profile_verification")
        academic_table = Table("academic_details")
        user_table = Table("users")
        volunteer = Table("users").as_("volunteer")

        query = (
            PostgreSQLQuery.from_(profile_table)
            .where(
                Criterion.all(
                    terms=[
                        profile_table.deleted_at.isnull(),
                        profile_table.status != "pending",
                    ]
                )
            )
            .join(volunteer)
            .on(profile_table.updated_by == volunteer.id)
            .join(academic_table)
            .on(profile_table.id == academic_table.id)
            .where(
                Criterion.all(
                    terms=[
                        academic_table.currently_enrolled == True,
                        academic_table.deleted_at.isnull(),
                    ]
                )
            )
            .join(user_table)
            .on(academic_table.id == user_table.id)
            .where(user_table.deleted_at.isnull())
            .select(
                user_table.id.as_("id"),
                user_table.name.as_("name"),
                user_table.sequence_number.as_("sequence_number"),
                user_table.role.as_("role"),
                academic_table.institution_name.as_("institution_name"),
                academic_table.course_stream_specialization.as_("course"),
                academic_table.level_of_education.as_("level_of_education"),
                academic_table.current_semester.as_("semester"),
                profile_table.status.as_("status"),
                profile_table.updated_by.as_("volunteer_id"),
                volunteer.name.as_("volunteer_name"),
                volunteer.sequence_number.as_("volunteer_sequence_number"),
            )
        )
        query = self._query_with_filters(query, filters)

        return await self.paginate_query(
            sql=query,
            values=(),
            dto_class=VerifiedDTO,
            page_meta=page_meta,
            connection=connection,
        )


async def main():
    db = DBManager()
    await db.init_pool()

    repo = VerificationReadRepository(db)

    verified_entries = await repo.verified_entries(
        filters=VerifiedFilters(),
        page_meta=PageMeta(),
        connection=None,
    )

    print(verified_entries)

    await db.close_pool()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
