from uuid import UUID

from src.core.storage.s3 import FileMetadata, S3Bucket
from src.exceptions import ProfileVerificationNotFoundError
from src.query.dto.base import PageMeta, Paginated
from src.query.dto.profile_verification import (
    GetParticular,
    GetParticularRecordResponse,
    GetVerifiedParticularResponse,
    VerificationDTO,
    VerificationFilters,
    VerifiedDTO,
    VerifiedFilters,
)
from src.query.repositories.profile_verification import VerificationReadRepository


class VerificationReadService:
    def __init__(
        self, verification_repo: VerificationReadRepository, file_service: S3Bucket
    ):
        self.verification_repo = verification_repo
        self.file_service = file_service

    async def get_pending_verifications(
        self, filters: VerificationFilters, page_meta: PageMeta
    ) -> Paginated[VerificationDTO]:
        return await self.verification_repo.pending_verification(
            filters=filters, page_meta=page_meta
        )

    async def get_verified_entries(
        self, filters: VerifiedFilters, page_meta: PageMeta
    ) -> Paginated[VerifiedDTO]:
        return await self.verification_repo.verified_entries(
            filters=filters, page_meta=page_meta
        )

    async def get_particular_record(self, user_id: UUID) -> GetParticularRecordResponse:
        record: (
            GetParticular | None
        ) = await self.verification_repo.get_particular_record(user_id=user_id)
        if not record:
            raise ProfileVerificationNotFoundError(
                f"no profile verification record found with this {user_id}"
            )
        media_url = await self.file_service.get_view_url(
            FileMetadata(
                key=record.storage_key,
                filename=record.filename,
                content_type=record.content_type,
            )
        )

        return GetParticularRecordResponse(media_url=media_url, **record.model_dump())

    async def get_verified_particular_record(
        self, user_id: UUID
    ) -> GetVerifiedParticularResponse:

        record: (
            GetParticular | None
        ) = await self.verification_repo.get_verified_particular_record(user_id=user_id)
        if not record:
            raise ProfileVerificationNotFoundError(
                f"no profile verification record found with this {user_id}"
            )
        media_url = await self.file_service.get_view_url(
            FileMetadata(
                key=record.storage_key,
                filename=record.filename,
                content_type=record.content_type,
            )
        )

        return GetVerifiedParticularResponse(media_url=media_url, **record.model_dump())
