"""
Why this setting.py ?
- Help manage environment variables and settings for the application.
Here we store the env variable by grouping them into classes.
It uses pydantic and pydantic-settings to validate and load settings from environment variables.
It layer only responsible for env values.
- Helps to maintain all environment variables in one place.
"""

from typing import Annotated

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class FrontendSettings(BaseSettings):
    url: str
    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="FRONTEND_", extra="ignore"
    )


class MicrosoftSettings(BaseSettings):
    client_id: str
    client_secret: str
    server_metadata_url: str

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="MICROSOFT_", extra="ignore"
    )


class GitHubSettings(BaseSettings):
    client_id: str
    client_secret: str
    authorize_url: str
    access_token_url: str
    api_base_url: str

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="GITHUB_", extra="ignore"
    )


class GoogleSettings(BaseSettings):
    client_id: str
    client_secret: str
    server_metadata_url: str

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="GOOGLE_", extra="ignore"
    )


class JWTSettings(BaseSettings):
    secret_key: SecretStr
    algorithm: str = "HS256"
    expire_mins: int = 4320  # 3 days.

    model_config = SettingsConfigDict(
        env_file="src/.env", extra="ignore", env_prefix="JWT_"
    )


class EmailVerification(BaseSettings):
    secret_key: SecretStr
    salt: SecretStr
    token_expire_seconds: int = 600

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="EMAIL_VERIFICATION_", extra="ignore"
    )


class DatabaseSettings(BaseSettings):
    name: SecretStr
    host: SecretStr
    port: int
    password: SecretStr
    user: SecretStr
    min_conn: int
    max_conn: int

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="DATABASE_", extra="ignore"
    )


class PincodeSettings(BaseSettings):
    api_url: str

    model_config = SettingsConfigDict(
        env_file="src/.env", env_prefix="PINCODE_", extra="ignore"
    )


class Settings(BaseModel):
    database: Annotated[DatabaseSettings, Field(default_factory=DatabaseSettings)]  # type: ignore[arg-type]
    jwt: Annotated[JWTSettings, Field(default_factory=JWTSettings)]  # type: ignore[arg-type]
    google: Annotated[GoogleSettings, Field(default_factory=GoogleSettings)]  # type: ignore[arg-type]
    github: Annotated[GitHubSettings, Field(default_factory=GitHubSettings)]  # type: ignore[arg-type]
    microsoft: Annotated[MicrosoftSettings, Field(default_factory=MicrosoftSettings)]  # type: ignore[arg-type]
    email_verification: Annotated[
        EmailVerification, Field(default_factory=EmailVerification)  # type: ignore[arg-type]
    ]
    reset_password: Annotated[
        EmailVerification, Field(default_factory=EmailVerification)  # type: ignore[arg-type]
    ]
    frontend: Annotated[FrontendSettings, Field(default_factory=FrontendSettings)]  # type: ignore[arg-type]
    # pincode: Annotated[PincodeSettings, Field(default_factory=PincodeSettings)]  # type: ignore[arg-type]

    pincode: Annotated[PincodeSettings, Field(default_factory=PincodeSettings)]  # type: ignore[arg-type]


settings = Settings()  # type: ignore[call-arg]
