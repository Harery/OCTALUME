"""Configuration management for OCTALUME."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_prefix="OCTALUME_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "OCTALUME"
    app_version: str = "2.0.0"
    debug: bool = False

    log_level: str = "INFO"
    log_json: bool = False

    state_dir: Path = Field(default=Path(".octalume"))

    web_host: str = "0.0.0.0"
    web_port: int = 8000

    database_url: str | None = None
    redis_url: str | None = None

    anthropic_api_key: str | None = None

    default_compliance_standards: list[str] = Field(default_factory=list)

    agent_timeout_seconds: int = 3600
    agent_max_retries: int = 3


_settings: Settings | None = None


def get_settings() -> Settings:
    """Get application settings (singleton)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
