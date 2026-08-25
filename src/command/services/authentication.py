from typing import ClassVar, cast

from asyncpg import Connection
from itsdangerous import BadSignature, SignatureExpired

from src.api.schemas.authentication import (
    ContextFromProvider,
    ForgotPassword,
    Login,
    LoginResponseSchema,
)
from src.command.commands.authentication import (
    EmailVerificationContext,
    GetUserByToken,
    ResetPasswordByToken,
    ResetPasswordContext,
    UpdateLastLogin,
    UserContext,
    VerifyEmailByToken,
)
from src.command.commands.providers import ProviderCreate, ProviderGet
from src.command.commands.users import (
    User,
    UserCreate,
    UserGetByEmail,
    UserGetById,
    UserRole,
    UserUpdate,
)
from src.command.repositories.providers import ProviderRepository
from src.command.repositories.users import UserRepository
from src.command.services.base import BaseService
from src.core.security.jwt import JWTHandler, JWTPayloadCreate
from src.core.security.password import PasswordHasher
from src.core.security.serializer import (
    reset_password_serializer,
    verify_email_serializer,
)
from src.exceptions import (
    BadTokenError,
    EmailNotVerifiedError,
    EmailVerificationError,
    ExpiredTokenError,
    InvalidCredentialsError,
    NotFoundException,
    PasswordNotFoundError,
    UnAuthenticatedError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.settings import settings


class AuthenticationService(BaseService[User]):
    _not_found_exc: ClassVar[type[NotFoundException]] = UserNotFoundError

    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        jwt_handler: JWTHandler,
        provider_repo: ProviderRepository,
    ) -> None:
        self.user_repo: UserRepository = user_repo
        self.password_hasher: PasswordHasher = password_hasher
        self.jwt_handler: JWTHandler = jwt_handler
        self.provider_repo: ProviderRepository = provider_repo

    async def _update_last_login(
        self, cmd: UpdateLastLogin, connection: Connection | None = None
    ) -> User:
        return self._require_entity(
            await self.user_repo.update_last_login(cmd=cmd, connection=connection)
        )

    async def signup(self, cmd: UserCreate) -> User:
        """Registers a new user with the given details."""

        if await self.user_repo.get(UserGetByEmail(email=cmd.email)):
            raise UserAlreadyExistsError(
                message=f"Account Already Exists with email: {cmd.email}"
            )

        hashed_password = self.password_hasher.hash_password(cast(str, cmd.password))
        return await self.user_repo.add(
            UserCreate(name=cmd.name, email=cmd.email, password=hashed_password)
        )

    async def login(self, cmd: Login) -> str:
        """Login a user with the given credentials."""

        user = await self.user_repo.get(UserGetByEmail(email=cmd.email))

        if user is None:
            raise InvalidCredentialsError(message="Incorrect Email or Password.")

        if user.password is None:
            raise PasswordNotFoundError(message="Password not found.")

        if not self.password_hasher.verify_password(
            raw_password=cmd.password, hashed_password=user.password
        ):
            raise InvalidCredentialsError(message="Incorrect Email or Password.")

        if not user.email_verified:
            raise EmailNotVerifiedError(message="Email not verified.")

        _ = await self._update_last_login(UpdateLastLogin(user_id=user.id))

        # Encode the JWT token and return it.
        return self.jwt_handler.create_jwt_token(
            payload=JWTPayloadCreate(user_id=user.id, role=user.role)
        )

    async def generate_email_verification_token(
        self, email: str
    ) -> EmailVerificationContext:
        """
        Generates an email verification token for the given email.
        """
        user = await self.user_repo.get(UserGetByEmail(email=email))

        if user is None:
            raise self._not_found_exc(message=f"User not found with the email: {email}")

        if user.email_verified:
            raise EmailVerificationError(message="Email already verified.")

        token = verify_email_serializer.dumps({"email": email})
        return EmailVerificationContext(name=user.name, token=token)

    async def verify_email(self, cmd: VerifyEmailByToken) -> str:
        """
        Verifies the email using the given token.
        """

        try:
            payload = verify_email_serializer.loads(  # pyright: ignore[reportAny]
                cmd.token, max_age=settings.email_verification.token_expire_seconds
            )
            user = await self.user_repo.get(UserGetByEmail(email=payload.get("email")))  # pyright: ignore[reportAny]

            if user is None:
                raise self._not_found_exc(
                    message=f"User not found with the email: {payload.get('email')}"  # pyright: ignore[reportAny]
                )

            # If not verified.
            if not user.email_verified:
                user = await self.user_repo.update(
                    cmd=UserUpdate(id=user.id, email_verified=True, updated_by=user.id)
                )
                user = self._require_entity(user)

            _ = await self._update_last_login(UpdateLastLogin(user_id=user.id))

            return self.jwt_handler.create_jwt_token(
                payload=JWTPayloadCreate(user_id=user.id, role=user.role)
            )

        except SignatureExpired:
            raise ExpiredTokenError(message="Email verification token has expired")
        except BadSignature:
            raise BadTokenError(message="Invalid email verification token")

    async def generate_set_password_token(
        self, cmd: ForgotPassword
    ) -> ResetPasswordContext:
        """
        Sends a password reset token to the user's email.
        """

        user = await self.user_repo.get(UserGetByEmail(email=cmd.email))

        if user is None:
            raise self._not_found_exc(message=f"User not found: {cmd.email}")

        if not user.email_verified:
            raise EmailNotVerifiedError(message="Email not verified.")

        token = reset_password_serializer.dumps({"email": cmd.email})

        return ResetPasswordContext(name=user.name, token=token)

    async def set_password(self, cmd: ResetPasswordByToken) -> User:
        """
        Resets the user's password using the provided token and new password.
        """

        # Verify the token.
        try:
            payload = reset_password_serializer.loads(  # pyright: ignore[reportAny]
                cmd.token, max_age=settings.reset_password.token_expire_seconds
            )
            user = await self.user_repo.get(UserGetByEmail(email=payload.get("email")))  # pyright: ignore[reportAny]
            if user is None:
                raise self._not_found_exc(message="User not found")

            hashed_password = self.password_hasher.hash_password(cmd.password)

            updated_user = await self.user_repo.update(
                cmd=UserUpdate(id=user.id, password=hashed_password, updated_by=user.id)
            )

            return self._require_entity(updated_user, value=user.id)

        except SignatureExpired:
            raise ExpiredTokenError(message="Reset password token has expired")
        except BadSignature:
            raise BadTokenError(message="Invalid reset password token")

    async def continue_with_oauth(
        self, cmd: ContextFromProvider
    ) -> LoginResponseSchema:

        user = await self.user_repo.get(UserGetByEmail(email=cmd.email))

        if user is None:
            # Signup with auto verification
            async with self.user_repo.db.transaction() as tconn:
                user = await self.user_repo.add(
                    cmd=UserCreate(
                        name=cmd.name,
                        email=cmd.email,
                        role=UserRole.STUDENT,
                        email_verified=True,
                    ),
                    connection=tconn,
                )
                _ = await self.provider_repo.add(
                    cmd=ProviderCreate(
                        name=cmd.provider_name,
                        user_id=user.id,
                        sub=cmd.sub,
                    ),
                    connection=tconn,
                )

            _ = await self._update_last_login(UpdateLastLogin(user_id=user.id))

            return LoginResponseSchema(
                access_token=self.jwt_handler.create_jwt_token(
                    payload=JWTPayloadCreate(user_id=user.id, role=user.role)
                ),
                last_login=user.last_login,
            )

        provider = await self.provider_repo.get(
            query=ProviderGet(name=cmd.provider_name, user_id=user.id)
        )

        if provider is None:
            async with self.user_repo.db.transaction() as tconn:
                _ = await self.provider_repo.add(
                    cmd=ProviderCreate(
                        name=cmd.provider_name,
                        user_id=user.id,
                        sub=cmd.sub,
                    ),
                    connection=tconn,
                )
                _ = await self.user_repo.update(
                    cmd=UserUpdate(id=user.id, email_verified=True, updated_by=user.id),
                    connection=tconn,
                )

                _ = await self._update_last_login(
                    UpdateLastLogin(user_id=user.id), connection=tconn
                )

        # return self.jwt_handler.create_jwt_token(
        #     payload=JWTPayloadCreate(user_id=user.id, role=user.role)
        # )

        return LoginResponseSchema(
            access_token=self.jwt_handler.create_jwt_token(
                payload=JWTPayloadCreate(user_id=user.id, role=user.role)
            ),
            last_login=user.last_login,
        )

    async def me(self, token: GetUserByToken) -> UserContext:
        """
        Returns the authenticated user's context.
        """
        payload = self.jwt_handler.decode_jwt_token(token=token.token)
        user = await self.user_repo.get(UserGetById(id=payload.user_id))

        if user is None:
            # raise self._not_found_exc(message=f"User not found: {payload.user_id}")
            raise UnAuthenticatedError(message=f"User not found: {payload.user_id}")

        return UserContext(
            user_id=user.id, username=user.name, email=user.email, role=user.role
        )
