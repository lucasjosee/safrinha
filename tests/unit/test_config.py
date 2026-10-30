import pytest
from pydantic import ValidationError

from safrinha.config import Settings

ENV_VARS = [
    "APP_ENV",
    "ANTHROPIC_API_KEY",
    "VOYAGE_API_KEY",
    "DATABASE_URL",
    "LLM_MODEL",
    "EMBEDDING_MODEL",
    "EMBEDDING_DIM",
]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    # Isolate tests from the developer's shell environment.
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def load_settings() -> Settings:
    # _env_file=None ignores the local .env, so only the test's env vars count.
    return Settings(_env_file=None)


def test_loads_without_credentials() -> None:
    settings = load_settings()

    assert settings.app_env == "development"
    assert settings.anthropic_api_key is None
    assert settings.voyage_api_key is None
    assert settings.database_url is None


def test_empty_value_is_treated_as_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EMBEDDING_DIM", "")

    assert load_settings().embedding_dim is None


def test_api_key_is_hidden_in_repr(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")

    settings = load_settings()

    assert "sk-test-123" not in repr(settings)
    assert settings.anthropic_api_key is not None
    assert settings.anthropic_api_key.get_secret_value() == "sk-test-123"


def test_rejects_unknown_app_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")

    with pytest.raises(ValidationError):
        load_settings()


def test_rejects_non_positive_embedding_dim(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EMBEDDING_DIM", "0")

    with pytest.raises(ValidationError):
        load_settings()
