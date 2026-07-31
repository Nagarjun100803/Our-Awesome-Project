"""
This module provides the exception registry for the API.
    - In this module we map the status codes to the respected exceptions.
"""

from http import HTTPStatus

import src.exceptions as exc

exception_registry: dict[type[exc.DomainException], HTTPStatus] = {
    exc.AuthenticationException: HTTPStatus.UNAUTHORIZED,  # 401
    exc.ValidationException: HTTPStatus.BAD_REQUEST,  # 400
    exc.NotFoundException: HTTPStatus.NOT_FOUND,  # 404
    exc.ConflictException: HTTPStatus.CONFLICT,  # 409
    exc.SecurityException: HTTPStatus.UNAUTHORIZED,  # 401
}
