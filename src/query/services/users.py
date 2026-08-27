from src.command.commands.users import UserRole
from src.query.dto.base import PageMeta, Paginated
from src.query.dto.users import UserDTO, UserFilters
from src.query.repositories.users import UserReadRepository


class UserReadService:
    def __init__(self, repository: UserReadRepository):
        self._repository = repository

    async def list_users(
        self, page_meta: PageMeta, filters: UserFilters
    ) -> Paginated[UserDTO]:
        return await self._repository.list_users(page_meta, filters)

    async def list_volunteers(self) -> list[UserDTO]:
        return await self._repository.get_user_by_role(
            filters=UserFilters(role=UserRole.VOLUNTEER)
        )
