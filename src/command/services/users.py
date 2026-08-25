import random
import string

from src.command.commands.users import User, UserCreate
from src.command.repositories.users import UserRepository
from src.command.services.base import BaseService
from src.core.email.email_service import EmailService
from src.core.email.models import AccountCreation
from src.core.security.password import PasswordHasher
from src.exceptions import UserAlreadyExistsError


class UserService(BaseService):
    def __init__(
        self,
        user_repo: UserRepository,
        email_service: EmailService,
        password_handler: PasswordHasher,
    ) -> None:
        self.repo = user_repo
        self.email_service = email_service
        self.password_handler = password_handler

    async def register(self, cmd: UserCreate, origin: str) -> User:
        # this method calls when the user created by admin
        # for that we need to create a automated password and send them in email\
        # we are not creating the password
        #
        if await self.repo.exists_by(email=cmd.email):
            raise UserAlreadyExistsError(f"User already exists with email{cmd.email}")
        password = self._gen_random_passcode()
        cmd.password = self.password_handler.hash_password(password)
        user = await self.repo.add(cmd=cmd)
        # self.background_task.add_task(
        #     self.email_service.send_template_one,
        #     context=AccountCreation(
        #         name=user.name,
        #         email=user.email,
        #         password=password,
        #         url=f"{origin}login",
        #     ),
        # )

        await self.email_service.send_template_one(
            context=AccountCreation(
                name=user.name,
                email=user.email,
                password=password,
                url=f"{origin}login",
            )
        )
        return user

    def _gen_random_passcode(self):
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))
