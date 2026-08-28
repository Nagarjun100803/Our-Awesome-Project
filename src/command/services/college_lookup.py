from src.api.schemas.profile_completion import CollegeLookupResponse
from src.command.commands.college_lookup import CollegeLookupGet
from src.command.repositories.college_lookup import CollegeLookupRepository


class CollegeLookupService:
    def __init__(self, repo: CollegeLookupRepository):
        self._repo = repo

    async def get(self, query: CollegeLookupGet) -> list[CollegeLookupResponse]:
        records = await self._repo.get(query)

        return [
            CollegeLookupResponse(
                name=record.name + ", " + record.district + ", " + record.state,
                university=record.university_name,
            )
            for record in records
        ]
