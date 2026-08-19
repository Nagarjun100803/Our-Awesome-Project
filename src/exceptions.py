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
    error_code = "DOMAIN_ERROR"
    message = "Internal Server Errror"

    def __init__(self, message: str | None = None, **kwargs):
        if message:
            self.message = message
        super().__init__(self.message)


# Authentication Exceptions
"""
    Authentication Exceptions - Raised when authentication fails or is not provided.
"""


class AuthenticationException(DomainException):
    error_code = "AUTHENTICATION_ERROR"
    message = "Authentication failed"


class InvalidCredentialsError(AuthenticationException):
    error_code = "INVALID_CREDENTIALS"
    message = "Invalid Email or Password"


class InvalidTokenError(AuthenticationException):
    error_code = "INVALID_TOKEN"
    message = "Invalid Authentication Token"


class ExpiredTokenError(AuthenticationException):
    error_code = "EXPIRED_TOKEN"
    message = "Authentication Token is Expired"


class MissingTokenError(AuthenticationException):
    error_code = "MISSING_TOKEN"
    message = "Authentication Token is missing"


class BadTokenError(AuthenticationException):
    error_code = "BAD_TOKEN"
    message = "Invalid Authentication Token"


#   Not Found Exceptions
"""
    Not Found Exceptions - Raised when a resource is not found.
"""


class NotFoundException(DomainException):
    error_code = "NOT_FOUND"
    _entity = "Resource"
    message = f"{_entity} not found"

    def __init__(self, message: str | None = None, **kwargs):
        self.message = f"{self._entity} not found with"
        for key, value in kwargs.items():
            self.message = self.message + f"{key}: {value} , "
        if message is None:
            super().__init__(self.message)
        else:
            super().__init__(message=message)


class UserNotFoundError(NotFoundException):
    error_code = "USER_NOT_FOUND"
    _entity = "User"


class OpenIDConnectNotFoundError(NotFoundException):
    error_code = "OPENID_CONNECT_NOT_FOUND"
    _entity = "OpenIDConnect"


class PasswordNotFoundError(NotFoundException):
    error_code = "PASSWORD_NOT_FOUND"
    _entity = "Password"


class PersonalDetailsNotFoundError(NotFoundException):
    error_code = "PERSONAL_DETAILS_NOT_FOUND"
    _entity = "PersonalDetails"


class AcademicDetailsNotFoundError(NotFoundException):
    error_code = "ACADEMIC_DETAILS_NOT_FOUND"
    _entity = "AcademicDetails"


class AcademicWithEnrollmentsNotFoundError(NotFoundException):
    error_code = "ACADEMIC_WITH_ENROLLMENTS_NOT_FOUND"
    _entity = "AcademicDetails with Enrollment not found"


class ParentalDetailsNotFoundError(NotFoundException):
    error_code = "PARENTAL_DETAILS_NOT_FOUND"
    _entity = "ParentalDetails"


class PincodeNotFoundError(NotFoundException):
    error_code = "PINCODE_NOT_FOUND"
    _entity = "Pincode"


class MediaNotFoundError(NotFoundException):
    error_code = "MEDIA_NOT_FOUND"
    _entity = "Media"


class ProfileVerificationNotFoundError(NotFoundException):
    error_code = "PROFILE_VERIFICATION_NOT_FOUND"
    _entity = "ProfileVerification"


# conflict Exceptions:
"""
    Conflict Exceptions - Raised when a conflict occurs, such as a duplicate resource.
"""


class ConflictException(DomainException):
    pass


class EmailVerificationError(ConflictException):
    error_code = "EMAIL_VERIFICATION_ERROR"
    message = "Email verification error"


class UserAlreadyExistsError(ConflictException):
    error_code = "USER_ALREADY_EXISTS"
    message = "User Already Exists"


class PersonalDetailsAlreadyExistsError(ConflictException):
    error_code = "PERSONAL_DETAILS_ALREADY_EXISTS"
    message = "Personal details already exists"


class AcademicDetailsAlreadyExistsError(ConflictException):
    error_code = "ACADEMIC_DETAILS_ALREADY_EXISTS"
    message = "Academic details already exists"


class ParentalDetailsAlreadyExistsError(ConflictException):
    error_code = "PARENTAL_DETAILS_ALREADY_EXISTS"
    message = "Parental details already exists"


#   Validation Exceptions
class ValidationException(DomainException):
    error_code = "VALIDATION_ERROR"
    message = "Validation failed"


class PasswordConfirmMismatchError(ValidationException):
    error_code = "INVALID_PASSWORD_CONFIRMATION"
    message = "Password and confirmation do not match"


class NameLengthError(ValidationException):
    error_code = "NAME_LENGTH_ERROR"
    message = "Name length is invalid"


class AcademicDetailsNotUnique(ValidationException):
    error_code = "ACADEMIC_DETAILS_NOT_UNIQUE"
    message = "Academic details are not unique"


class ParentalDetailsError(ValidationException):
    error_code = "PARENTAL_DETAILS_ERROR"
    message = "Only one of father, mother, or guardian can be provided"


"""
Security Errors - Authorization Related Errors
"""


class SecurityException(DomainException):
    """Base class for authentication and authorization errors."""

    error_code = "SECURITY_ERROR"

    message = "A Security error occurred."


class EmailNotVerifiedError(SecurityException):
    error_code = "EMAIL_NOT_VERIFIED"
    message = "Email not verified."


class UnAuthorizedError(SecurityException):
    error_code = "UNAUTHORIZED"
    message = "Unauthorized."


class UnAuthenticatedError(SecurityException):
    error_code = "UNAUTHENTICATED"
    message = "Unauthenticated."


"""
External Service Exceptions
Raised when an external/upstream service fails.
"""


class ExternalServiceException(DomainException):
    error_code = "EXTERNAL_SERVICE_ERROR"
    message = "External service error"


class PostalServiceError(ExternalServiceException):
    error_code = "POSTAL_SERVICE_ERROR"
    message = "Postal service is currently unavailable"
