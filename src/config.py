"""Модуль конфигурации проекта"""
from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Базовый класс для настроек проекта"""
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    DB_URL: str

    model_config = SettingsConfigDict(
        env_file=DOTENV/".env", arbitrary_types_allowed=True
    )

    @computed_field
    @property
    def TEMPLATES(self) -> Jinja2Templates:
        return Jinja2Templates(directory=(DOTENV/"src/templates"))


settings = Settings()
