from typing import Literal

from pydantic import PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, read from environment variables and `.env`.

    Service settings are optional here so the app and the tests start without
    real credentials. Each client checks the values it needs when it is created.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # `KEY=` in .env means "not set", so the field keeps its default.
        env_ignore_empty=True,
        # .env may hold variables for other tools, such as docker compose.
        extra="ignore",
    )

    app_env: Literal["development", "production"] = "development"

    # SecretStr keeps these values out of repr() and logs.
    anthropic_api_key: SecretStr | None = None
    voyage_api_key: SecretStr | None = None
    database_url: SecretStr | None = None

    llm_model: str | None = None
    embedding_model: str | None = None
    embedding_dim: PositiveInt | None = None
