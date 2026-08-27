from src.query.dto.base import PageMeta
from src.query.dto.profile_verification import VerificationFilters, VerifiedFilters
from src.query.repositories.profile_verification import VerificationReadRepository


class VerificationReadService:
    def __init__(self, verification_repo: VerificationReadRepository):
        self.verification_repo = verification_repo

    async def get_pending_verifications(
        self, filters: VerificationFilters, page_meta: PageMeta
    ):
        return await self.verification_repo.pending_verification(
            filters=filters, page_meta=page_meta
        )

    async def get_verified_entries(self, filters: VerifiedFilters, page_meta: PageMeta):
        return await self.verification_repo.verified_entries(
            filters=filters, page_meta=page_meta
        )
