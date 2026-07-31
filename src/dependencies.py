from src.command.repositories.providers import ProviderRepository
from src.command.repositories.users import UserRepository
from src.command.services.authentication import AuthenticationService
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
