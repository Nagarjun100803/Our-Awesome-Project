from uuid import UUID

from asyncpg import Connection
from pypika import Criterion, PostgreSQLQuery, Table
from pypika.enums import Order
from pypika.queries import QueryBuilder

from src.database import DBManager, ExecutableSQL
from src.query.dto.base import PageMeta, Paginated
from src.query.dto.profile_verification import (
    GetParticular,
    GetVerifiedParticular,
    VerificationDTO,
    VerificationFilters,
    VerifiedDTO,
    VerifiedFilters,
)
from src.query.repositories.mixins import PaginatorMixin

USERS = Table("users")
PROFILE_VERIFICATION = Table("profile_verification")
ACADEMIC_DETAILS = Table("academic_details")
PERSONAL_DETAILS = Table("personal_details")
MEDIA = Table("media")


class VerificationReadRepository(PaginatorMixin):
    def __init__(self, db: DBManager):
        self.db = db

    def _query_with_filters(
        self,
        query: QueryBuilder,
        filters: VerificationFilters | VerifiedFilters,
    ) -> QueryBuilder:
        if filters.name_or_email:
            query = query.where(
                Criterion.any(
                    terms=[
                        USERS.name.like(f"%{filters.name_or_email}%"),
                        USERS.email.like(f"%{filters.name_or_email}%"),
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
                query = query.where(PROFILE_VERIFICATION.status == filters.status)
            if filters.volunteer_id:
                query = query.where(
                    PROFILE_VERIFICATION.updated_by == filters.volunteer_id
                )

        return query

    def _base_profile_query(self) -> QueryBuilder:

        query = (
            PostgreSQLQuery.from_(PROFILE_VERIFICATION)
            .where(PROFILE_VERIFICATION.deleted_at.isnull())
            .join(ACADEMIC_DETAILS)
            .on(PROFILE_VERIFICATION.id == ACADEMIC_DETAILS.id)
            .where(
                Criterion.all(
                    terms=[
                        ACADEMIC_DETAILS.currently_enrolled == True,
                        ACADEMIC_DETAILS.deleted_at.isnull(),
                    ]
                )
            )
            .join(USERS)
            .on(ACADEMIC_DETAILS.id == USERS.id)
            .where(USERS.deleted_at.isnull())
        )
        return query

    @staticmethod
    def _core_columns():
        return [
            USERS.id.as_("id"),
            USERS.name.as_("name"),
            USERS.sequence_number.as_("student_sequence_number"),
            USERS.role.as_("role"),
            ACADEMIC_DETAILS.institution_name.as_("institution_name"),
            ACADEMIC_DETAILS.course_stream_specialization.as_("course"),
            ACADEMIC_DETAILS.level_of_education.as_("level_of_education"),
            ACADEMIC_DETAILS.current_semester.as_("semester"),
        ]

    async def pending_verification(
        self,
        filters: VerificationFilters,
        page_meta: PageMeta,
        connection: Connection | None = None,
    ) -> Paginated[VerificationDTO]:
        query = (
            self._base_profile_query()
            .where(PROFILE_VERIFICATION.status == "pending")
            .select(
                *self._core_columns(),
                PROFILE_VERIFICATION.created_at.as_("submitted_on"),
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
        volunteer = USERS.as_("volunteer")

        query = (
            self._base_profile_query()
            .where(PROFILE_VERIFICATION.status != "pending")
            .join(volunteer)
            .on(PROFILE_VERIFICATION.verified_by == volunteer.id)
            .select(
                *self._core_columns(),
                PROFILE_VERIFICATION.status.as_("status"),
                PROFILE_VERIFICATION.verified_by.as_("volunteer_id"),
                volunteer.name.as_("volunteer_name"),
                volunteer.sequence_number.as_("volunteer_sequence_number"),
                volunteer.role.as_("volunteer_role"),
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

    def _particular_record_query(
        self,
        user_id: UUID,
        include_verified: bool = False,
    ) -> QueryBuilder:
        query = (
            PostgreSQLQuery.from_(PROFILE_VERIFICATION)
            .where(PROFILE_VERIFICATION.id == user_id)
            .where(PROFILE_VERIFICATION.deleted_at.isnull())
            .join(ACADEMIC_DETAILS)
            .on(PROFILE_VERIFICATION.id == ACADEMIC_DETAILS.id)
            .where(
                Criterion.all(
                    terms=[
                        ACADEMIC_DETAILS.currently_enrolled == True,
                        ACADEMIC_DETAILS.deleted_at.isnull(),
                    ]
                )
            )
            .join(PERSONAL_DETAILS)
            .on(PROFILE_VERIFICATION.id == PERSONAL_DETAILS.id)
            .join(MEDIA)
            .on(MEDIA.id == PROFILE_VERIFICATION.media_id)
            .where(
                Criterion.all(
                    terms=[
                        MEDIA.status == "uploaded",
                        MEDIA.deleted_at.isnull(),
                    ]
                )
            )
            .join(USERS)
            .on(PROFILE_VERIFICATION.id == USERS.id)
            .where(USERS.deleted_at.isnull())
        )

        columns = [
            USERS.name.as_("name"),
            PERSONAL_DETAILS.dob.as_("dob"),
            PERSONAL_DETAILS.phone.as_("contact_number"),
            PERSONAL_DETAILS.street.as_("address"),
            PERSONAL_DETAILS.city.as_("city"),
            PERSONAL_DETAILS.district.as_("district"),
            PERSONAL_DETAILS.state.as_("state"),
            PERSONAL_DETAILS.pincode.as_("pincode"),
            ACADEMIC_DETAILS.level_of_education.as_("current_education_level"),
            ACADEMIC_DETAILS.course_stream_specialization.as_(
                "course_stream_specialization"
            ),
            ACADEMIC_DETAILS.institution_name.as_("institution_name"),
            ACADEMIC_DETAILS.register_number.as_("register_number"),
            ACADEMIC_DETAILS.current_semester.as_("current_semester"),
            ACADEMIC_DETAILS.year_of_passing.as_("year_of_passing"),
            MEDIA.filename.as_("filename"),
            MEDIA.storage_key.as_("storage_key"),
            MEDIA.content_type.as_("content_type"),
            PROFILE_VERIFICATION.status.as_("status"),
        ]

        if include_verified:
            volunteer = USERS.as_("volunteer")
            query = (
                query.where(PROFILE_VERIFICATION.status != "pending")
                .join(volunteer)
                .on(PROFILE_VERIFICATION.verified_by == volunteer.id)
            )
            columns += [
                PROFILE_VERIFICATION.verified_by.as_("volunteer_id"),
                volunteer.name.as_("volunteer_name"),
                volunteer.sequence_number.as_("volunteer_sequence_number"),
                volunteer.role.as_("volunteer_role"),
            ]

        return query.select(*columns)

    async def _fetch_particular(
        self,
        query: QueryBuilder,
        dto_class: type,
        connection: Connection | None,
    ):
        executables = ExecutableSQL(sql=query.get_sql(), values=())
        record = await self.db.execute(
            executable=executables, fetch_returns="one", connection=connection
        )
        if not record:
            return None
        return dto_class.model_validate(dict(record))

    async def get_particular_record(
        self,
        user_id: UUID,
        connection: Connection | None = None,
    ) -> GetParticular | None:
        query = self._particular_record_query(user_id, include_verified=False)
        return await self._fetch_particular(query, GetParticular, connection)

    async def get_verified_particular_record(
        self,
        user_id: UUID,
        connection: Connection | None = None,
    ) -> GetVerifiedParticular | None:
        query = self._particular_record_query(user_id, include_verified=True)
        return await self._fetch_particular(query, GetVerifiedParticular, connection)


async def main():
    db = DBManager()

    await db.init_pool()

    repo = VerificationReadRepository(db)

    record = await repo.get_verified_particular_record(
        user_id=UUID("587b00ad-d687-4153-b428-49375fa03aa3")
    )

    print(record)
    await db.close_pool()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
