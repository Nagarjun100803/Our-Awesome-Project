from src.command.repositories.academic_details import AcademicDetailsRepository
from src.command.repositories.parental_details import ParentalDetailsRepository
from src.command.repositories.personal_details import PersonalDetailsRepository
from src.command.repositories.providers import ProviderRepository
from src.command.repositories.users import UserRepository
from src.command.services import profile_completion
from src.command.services.academic_details import AcademicDetailsService
from src.command.services.authentication import AuthenticationService
from src.command.services.parental_details import ParentalDetailsService
from src.command.services.personal_details import PersonalDetailsService
from src.core.security.jwt import JWTHandler
from src.core.security.password import PasswordHasher
from src.database import DBManager

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

profile_completion_service = profile_completion.ProfileCompletionService(
    personal_service=personal_service,
    academic_service=academic_service,
    parental_service=parental_service,
)
