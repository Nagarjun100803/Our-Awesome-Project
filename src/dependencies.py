from src.command.repositories.academic_details import AcademicDetailsRepository
from src.command.repositories.college_lookup import CollegeLookupRepository
from src.command.repositories.media import MediaRepository
from src.command.repositories.parental_details import ParentalDetailsRepository
from src.command.repositories.personal_details import PersonalDetailsRepository
from src.command.repositories.profile_verification import ProfileVerificationRepository
from src.command.repositories.providers import ProviderRepository
from src.command.repositories.users import UserRepository
from src.command.services.academic_details import AcademicDetailsService
from src.command.services.authentication import AuthenticationService
from src.command.services.college_lookup import CollegeLookupService
from src.command.services.location_lookup import LocationLookupService
from src.command.services.media import MediaService
from src.command.services.parental_details import ParentalDetailsService
from src.command.services.personal_details import PersonalDetailsService
from src.command.services.profile_verification import ProfileVerificationService
from src.command.services.verify_profile_completion import (
    VerifyProfileCompletionService,
)
from src.core.email import email_service
from src.core.security.jwt import JWTHandler
from src.core.security.password import PasswordHasher
from src.core.storage.s3 import S3Bucket, get_session
from src.database import DBManager
from src.settings import settings

"""
Database Dependencies
"""
db = DBManager()


"""
Repository Dependencies
"""
user_repo = UserRepository(db=db)
provider_repo = ProviderRepository(db=db)
personal_repo = PersonalDetailsRepository(db=db)
academic_repo = AcademicDetailsRepository(db=db)
parental_repo = ParentalDetailsRepository(db=db)

"""
Core/Security Dependencies
"""
jwt_handler = JWTHandler()
password_hasher = PasswordHasher()


"""
Service related Dependencies
"""
authentication_service = AuthenticationService(
    user_repo=user_repo,
    jwt_handler=jwt_handler,
    password_hasher=password_hasher,
    provider_repo=provider_repo,
)

personal_service = PersonalDetailsService(repo=personal_repo)
academic_service = AcademicDetailsService(repo=academic_repo)
parental_service = ParentalDetailsService(repo=parental_repo)


verify_profile_completion_service = VerifyProfileCompletionService(
    personal_service=personal_service,
    academic_service=academic_service,
    parental_service=parental_service,
)


"""
Location Lookup Dependencies
"""

location_lookup_service = LocationLookupService()


"""
College Lookup Dependencies
"""
college_lookup_repo = CollegeLookupRepository(db=db)
college_lookup_service = CollegeLookupService(repo=college_lookup_repo)


"""S3 Dependencies
"""
s3_bucket = S3Bucket(bucket_name=settings.s3.bucket, session=get_session())


"""
Email Dependencies
"""

email_service = email_service.EmailService(
    provider=email_service.SMTPEmailProvider(),
    renderer=email_service.EmailTemplateRenderer(),
)


"""
Profile Verification Dependencies
"""
profile_verification_repo = ProfileVerificationRepository(db=db)
media_repo = MediaRepository(db=db)
media_service = MediaService(repo=media_repo)
profile_verification_service = ProfileVerificationService(
    repo=profile_verification_repo,
    media_service=media_service,
    file_service=s3_bucket,
)
