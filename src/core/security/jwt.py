from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import BaseModel

from src.command.commands.users import UserRole
from src.exceptions import ExpiredTokenError, InvalidTokenError
from src.settings import settings


class JWTPayloadCreate(BaseModel):
    user_id: UUID
    role: UserRole


class JWTPayload(JWTPayloadCreate):
    sub: str = "access_token"
    exp: int


class JWTHandler:
    def create_jwt_token(
        self, payload: JWTPayloadCreate, expires_delta: timedelta | None = None
    ) -> str:

        if expires_delta is None:
            exp = datetime.now(tz=UTC) + timedelta(minutes=settings.jwt.expire_mins)
        else:
            exp = datetime.now(tz=UTC) + expires_delta

        data = payload.model_copy().model_dump(mode="json")
        data.update({"sub": "access_token", "exp": exp})
        return jwt.encode(
            data,
            algorithm=settings.jwt.algorithm,
            key=settings.jwt.secret_key.get_secret_value(),
        )

    def decode_jwt_token(self, token: str) -> JWTPayload:
        try:
            payload = jwt.decode(
                token,
                key=settings.jwt.secret_key.get_secret_value(),
                algorithms=[settings.jwt.algorithm],
            )
            return JWTPayload(**payload)

        except ExpiredSignatureError:
            raise ExpiredTokenError(message="JWT Token is Expired")
        except JWTError:
            raise InvalidTokenError(message="Invalid JWT Token")


if __name__ == "__main__":
    jwt_handler = JWTHandler()
    token = jwt_handler.create_jwt_token(
        JWTPayloadCreate(user_id=UUID(int=1), role=UserRole.STUDENT)
    )
    print(token)
