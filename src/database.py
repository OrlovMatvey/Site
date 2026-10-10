"""Модуль для инициализации базы данных"""
from sqlalchemy import create_engine

from src.auth import Base
from src.config import settings

engine = create_engine(settings.DB_URL, echo=True)


def create_db() -> None:
    """Создание и обновление БД"""
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
