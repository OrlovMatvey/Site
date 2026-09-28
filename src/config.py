"""Модуль конфигурации проекта"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Базовый класс для настроек проекта"""
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    DB_URL: str

    model_config = SettingsConfigDict(env_file=DOTENV/".env")


settings = Settings()
