"""Модуль для инициализации базы данных"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_engine(settings.DB_URL, echo=True)


class Base(DeclarativeBase):
    """Базовый класс для моделей"""
    @classmethod
    def get_table_fields(cls) -> list:
        """Вывод полей для модели

        Returns:
            list: Список полей модели
        """
        return [a.name for a in cls.__table__.columns]
