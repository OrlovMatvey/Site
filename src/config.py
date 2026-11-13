"""Модуль конфигурации проекта"""
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Базовый класс для настроек проекта"""
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    DB_URL: str
    MASTER_URL: str
    DB_NAME: str
    TEMPLATES_DIR: Path = Field(DOTENV/"src/templates")
    STATIC_DIR: Path = Field(DOTENV/"src/static")

    model_config = SettingsConfigDict(
        env_file=DOTENV/".env", arbitrary_types_allowed=True
    )


settings = Settings()
