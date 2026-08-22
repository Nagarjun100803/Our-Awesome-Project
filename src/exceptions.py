"""
Why i dont use status codes here.
Why we need to map the status code for the respective exceptions in exception_registry.py in api layer
 - API layer is the responsible for request, response and status codes for that we used the exception_registry.py for mapping.
 - why not here: Because we want to keep the exceptions clean and separate from the status codes.
 - Every layer has its own responsibility and status codes should be handled at the API layer.

 Architecture:
     Service -> Raise the Exceptions
     In main -> Catch the Exceptions using exception_handler(we declared universal global exception handler) - This enables Global exception handling.
     In exception_handler -> Map the Exceptions to status codes(we get the status code from the exception registry)
     In exception_handler -> Return the status code and message to the client
"""

# Domain Exceptions
"""
    Base Exception for all domain exceptions.
"""


class DomainException(Exception):
    error_code: str = "DOMAIN_ERROR"
    message: str = "Internal Server Errror"

    def __init__(self, message: str | None = None, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        if message:
            self.message = message
        super().__init__(self.message)


# Authentication Exceptions
"""
    Authentication Exceptions - Raised when authentication fails or is not provided.
"""


class AuthenticationException(DomainException):
    error_code: str = "AUTHENTICATION_ERROR"
    message: str = "Authentication failed"


class InvalidCredentialsError(AuthenticationException):
    error_code: str = "INVALID_CREDENTIALS"
    message: str = "Invalid Email or Password"


class InvalidTokenError(AuthenticationException):
    error_code: str = "INVALID_TOKEN"
    message: str = "Invalid Authentication Token"


class ExpiredTokenError(AuthenticationException):
    error_code: str = "EXPIRED_TOKEN"
    message: str = "Authentication Token is Expired"


class MissingTokenError(AuthenticationException):
    error_code: str = "MISSING_TOKEN"
    message: str = "Authentication Token is missing"


class BadTokenError(AuthenticationException):
    error_code: str = "BAD_TOKEN"
    message: str = "Invalid Authentication Token"


#   Not Found Exceptions
"""
    Not Found Exceptions - Raised when a resource is not found.
"""


class NotFoundException(DomainException):
    error_code: str = "NOT_FOUND"
    _entity: str = "Resource"
    message: str = f"{_entity} not found"

    def __init__(self, message: str | None = None, **kwargs):  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        if message is None:
            super().__init__(self.message)  # pyright: ignore[reportUnknownMemberType]
        else:
            super().__init__(message=message)  # pyright: ignore[reportUnknownMemberType]


class UserNotFoundError(NotFoundException):
    error_code: str = "USER_NOT_FOUND"
    _entity: str = "User"


class OpenIDConnectNotFoundError(NotFoundException):
    error_code: str = "OPENID_CONNECT_NOT_FOUND"
    _entity: str = "OpenIDConnect"


class PasswordNotFoundError(NotFoundException):
    error_code: str = "PASSWORD_NOT_FOUND"
    _entity: str = "Password"


class PersonalDetailsNotFoundError(NotFoundException):
    error_code: str = "PERSONAL_DETAILS_NOT_FOUND"
    _entity: str = "PersonalDetails"


class AcademicDetailsNotFoundError(NotFoundException):
    error_code: str = "ACADEMIC_DETAILS_NOT_FOUND"
    _entity: str = "AcademicDetails"


class AcademicWithEnrollmentsNotFoundError(NotFoundException):
    error_code: str = "ACADEMIC_WITH_ENROLLMENTS_NOT_FOUND"
    _entity: str = "AcademicDetails with Enrollment not found"


class ParentalDetailsNotFoundError(NotFoundException):
    error_code: str = "PARENTAL_DETAILS_NOT_FOUND"
    _entity: str = "ParentalDetails"


class PincodeNotFoundError(NotFoundException):
    error_code: str = "PINCODE_NOT_FOUND"
    _entity: str = "Pincode"


class MediaNotFoundError(NotFoundException):
    error_code: str = "MEDIA_NOT_FOUND"
    _entity: str = "Media"


class ProfileVerificationNotFoundError(NotFoundException):
    error_code: str = "PROFILE_VERIFICATION_NOT_FOUND"
    _entity: str = "ProfileVerification"


# conflict Exceptions:
"""
    Conflict Exceptions - Raised when a conflict occurs, such as a duplicate resource.
"""


class ConflictException(DomainException):
    pass


class EmailVerificationError(ConflictException):
    error_code: str = "EMAIL_VERIFICATION_ERROR"
    message: str = "Email verification error"


class UserAlreadyExistsError(ConflictException):
    error_code: str = "USER_ALREADY_EXISTS"
    message: str = "User Already Exists"


class PersonalDetailsAlreadyExistsError(ConflictException):
    error_code: str = "PERSONAL_DETAILS_ALREADY_EXISTS"
    message: str = "Personal details already exists"


class AcademicDetailsAlreadyExistsError(ConflictException):
    error_code: str = "ACADEMIC_DETAILS_ALREADY_EXISTS"
    message: str = "Academic details already exists"


class ParentalDetailsAlreadyExistsError(ConflictException):
    error_code: str = "PARENTAL_DETAILS_ALREADY_EXISTS"
    message: str = "Parental details already exists"


#   Validation Exceptions
class ValidationException(DomainException):
    error_code: str = "VALIDATION_ERROR"
    message: str = "Validation failed"


class PasswordConfirmMismatchError(ValidationException):
    error_code: str = "INVALID_PASSWORD_CONFIRMATION"
    message: str = "Password and confirmation do not match"


class NameLengthError(ValidationException):
    error_code: str = "NAME_LENGTH_ERROR"
    message: str = "Name length is invalid"


class AcademicDetailsNotUnique(ValidationException):
    error_code: str = "ACADEMIC_DETAILS_NOT_UNIQUE"
    message: str = "Academic details are not unique"


class ParentalDetailsError(ValidationException):
    error_code: str = "PARENTAL_DETAILS_ERROR"
    message: str = "Only one of father, mother, or guardian can be provided"


class ProfileVerificationAlreadyExistsError(ConflictException):
    error_code: str = "PROFILE_VERIFICATION_ALREADY_EXISTS"
    message: str = "Profile verification already exists"


"""
Security Errors - Authorization Related Errors
"""


class SecurityException(DomainException):
    """Base class for authentication and authorization errors."""

    error_code: str = "SECURITY_ERROR"

    message: str = "A Security error occurred."


class EmailNotVerifiedError(SecurityException):
    error_code: str = "EMAIL_NOT_VERIFIED"
    message: str = "Email not verified."


class UnAuthorizedError(SecurityException):
    error_code: str = "UNAUTHORIZED"
    message: str = "Unauthorized."


class UnAuthenticatedError(SecurityException):
    error_code: str = "UNAUTHENTICATED"
    message: str = "Unauthenticated."


"""
External Service Exceptions
Raised when an external/upstream service fails.
"""


class ExternalServiceException(DomainException):
    error_code: str = "EXTERNAL_SERVICE_ERROR"
    message: str = "External service error"


class PostalServiceError(ExternalServiceException):
    error_code: str = "POSTAL_SERVICE_ERROR"
    message: str = "Postal service is currently unavailable"
