"""Модуль создания таблиц в БД"""
from sqlalchemy import create_engine, text

import src.auth
import src.recipe_service
from src.config import settings
from src.database import Base, engine


def init_database():
    """Функция создания БД и таблиц"""

    master_engine = create_engine(
        settings.MASTER_URL, isolation_level="AUTOCOMMIT"
    )

    check_query = text(
        f"SELECT database_id FROM sys.databases WHERE name = '{settings.DB_NAME}'"
    )

    with master_engine.connect() as conn:
        db_exists = conn.scalar(check_query)

        if not db_exists:
            print("DataBase not found")
            conn.execute(text(f"CREATE DATABASE [{settings.DB_NAME}]"))
            print("DataBase successful created")
        else:
            print("DataBase already exists")

    master_engine.dispose()

    Base.metadata.create_all(engine)
    print("Tables successful created")


if __name__ == "__main__":
    init_database()
