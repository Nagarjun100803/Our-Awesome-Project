import asyncio
from uuid import UUID

from src.command.commands.academic_details import (
    AcademicDetailsGetAll,
)
from src.command.commands.parental_details import (
    ParentalDetailsGet,
)
from src.command.commands.personal_details import (
    PersonalDetailsGet,
)
from src.command.services.academic_details import AcademicDetailsService
from src.command.services.parental_details import ParentalDetailsService
from src.command.services.personal_details import PersonalDetailsService


class VerifyProfileCompletionService:
    def __init__(
        self,
        personal_service: PersonalDetailsService,
        parental_service: ParentalDetailsService,
        academic_service: AcademicDetailsService,
    ) -> None:
        self.personal_service = personal_service
        self.parental_service = parental_service
        self.academic_service = academic_service

    async def is_completed(self, id: UUID):
        """
        If i get the userId then i will find is they complete or not
        """
        records = await asyncio.gather(
            self.personal_service.exists_by(cmd=PersonalDetailsGet(id=id)),
            self.academic_service.exists_by(cmd=AcademicDetailsGetAll(id=id)),
            self.parental_service.exists_by(cmd=ParentalDetailsGet(id=id)),
        )

        return records  # [true, true, true]
