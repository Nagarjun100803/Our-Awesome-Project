from typing import Any, ClassVar

from src.exceptions import NotFoundException


class BaseService[T]:
    """
    Base class for all the service. Do not use it directly.
    """

    _not_found_exc: ClassVar[type[NotFoundException]]
    _entity: ClassVar[str]

    def _require_entity(self, entity: T | None, **error_kwargs: Any) -> T:
        """
        Helper function that return the entity if not None.
        Otherwise it raise NotFoundError.
        Usefull only while checking after updating the field because we use exists_by mostly to check the data is found or not.
        """
        if entity is None:
            raise self._not_found_exc(**error_kwargs)
        return entity
