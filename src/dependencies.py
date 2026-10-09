"""Модуль за зависимостей FastAPI"""
from collections.abc import Iterator

from sqlalchemy.orm import Session, sessionmaker

from database import engine

session = sessionmaker(engine)


def get_db() -> Iterator[Session]:
    """Создание сессии БД

    Yields:
        Iterator[Session]: Объект сессии БД
    """
    try:
        db = session()
        yield db
    finally:
        db.close()
