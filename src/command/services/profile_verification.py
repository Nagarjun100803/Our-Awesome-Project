from typing import cast
from uuid import UUID

from asyncpg import Connection

from src.command.commands.base import BaseCmd
from src.command.commands.media import (
    MediaCreate,
    MediaGet,
    MediaStatusEnum,
    MediaUpdate,
)
from src.command.commands.profile_verification import (
    ProfileVerification,
    ProfileVerificationCreate,
    ProfileVerificationGet,
)
from src.command.repositories.profile_verification import ProfileVerificationRepository
from src.command.services.base import BaseService
from src.command.services.media import MediaService
from src.core.storage.s3 import FileMetadata, S3Bucket
from src.exceptions import (
    ProfileVerificationNotFoundError,
)


class InitializeMedia(BaseCmd):
    created_by: UUID
    filename: str
    file_size: int
    content_type: str


class InitializeMediaResponse(BaseCmd):
    presigned_url: str
    media_id: UUID


class ProfileVerificationService(BaseService[ProfileVerification]):
    _not_found_exc = ProfileVerificationNotFoundError

    def __init__(
        self,
        repo: ProfileVerificationRepository,
        media_service: MediaService,
        file_service: S3Bucket,
    ) -> None:
        self.repo = repo
        self.media_service = media_service
        self.file_service = file_service

    def _get_storage_key(self, filename: str, user_id: UUID) -> str:
        return f"profile_verifications/{user_id}/{filename}"

    async def initialize(
        self, cmd: InitializeMedia, connection: Connection | None = None
    ) -> InitializeMediaResponse:
        """
        Initializes a media entity for profile verification and send upload url.
        """
        media_context = self.media_service._require_entity(
            await self.media_service.create(
                cmd=MediaCreate(
                    filename=cmd.filename,
                    file_size=cmd.file_size,
                    content_type=cmd.content_type,
                    created_by=cmd.created_by,
                    storage_key=self._get_storage_key(cmd.filename, cmd.created_by),
                    storage_provider="Supabase S3",
                    status=MediaStatusEnum.PENDING,
                ),
            )
        )
        upload_url = await self.file_service.get_upload_url(
            metadata=FileMetadata(
                key=self._get_storage_key(cmd.filename, cmd.created_by),
                filename=cmd.filename,
                content_type=cmd.content_type,
            )
        )

        return InitializeMediaResponse(
            presigned_url=upload_url,
            media_id=cast(UUID, media_context.id),
        )

    async def create(
        self, cmd: ProfileVerificationCreate, connection: Connection | None = None
    ) -> ProfileVerification:
        """
        Creates a profile verification entity when the upload is Sucess.
        """
        if await self.repo.exists_by(id=cmd.id):
            raise self._not_found_exc(
                message=f"Profile verification with id {cmd.id} already exists"
            )

        async with self.repo.db.transaction() as tconn:
            await self.media_service.update(
                cmd=MediaUpdate(
                    id=cmd.media_id,
                    status=MediaStatusEnum.UPLOADED,
                    updated_by=cmd.created_by,
                ),
                connection=tconn,
            )
            return await self.repo.add(cmd, tconn)

    async def get_file_url(
        self, cmd: ProfileVerificationGet, connection: Connection | None = None
    ) -> str:

        profile_verification_cmd = self._require_entity(
            await self.repo.get(cmd, connection)
        )

        media_cmd = self.media_service._require_entity(
            await self.media_service.get(MediaGet(id=profile_verification_cmd.media_id))
        )

        return await self.file_service.get_view_url(
            metadata=FileMetadata(
                key=media_cmd.storage_key,
                filename=media_cmd.filename,
                content_type=media_cmd.content_type,
            )
        )

    async def upload_failure(
        self, cmd: MediaUpdate, connection: Connection | None = None
    ):
        await self.media_service.update(cmd, connection)

    # async def create(
    #     self, cmd: ProfileVerificationCreate, connection: Connection | None = None
    # ) -> ProfileVerification:

    #     if self.repo.exists_by(id=cmd.id):
    #         raise self._not_found_exc(
    #             message=f"Profile verification with id {cmd.id} already exists"
    #         )

    #     return await self.repo.add(cmd, connection)

    # async def update(
    #     self, cmd: ProfileVerificationUpdate, connection: Connection | None = None
    # ) -> ProfileVerification:
    #     return self._require_entity(await self.repo.update(cmd, connection))

    # async def delete(
    #     self, cmd: ProfileVerificationDelete, connection: Connection | None = None
    # ) -> ProfileVerification:
    #     return self._require_entity(
    #         await self.repo.delete(cmd=cmd, connection=connection)
    #     )

    # async def get(
    #     self, cmd: ProfileVerificationGet, connection: Connection | None = None
    # ) -> ProfileVerification:
    #     return self._require_entity(
    #         await self.repo.get(query=cmd, connection=connection)
    #     )
