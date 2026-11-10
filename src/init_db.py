"""Модуль создания таблиц в БД"""
from src.auth import UserData, UserTokenData
from src.database import Base, engine
from src.recipe_service import (
    CategoryData,
    CommentData,
    FavoriteRecipeData,
    IngredientData,
    RecipeData,
)

DB_NAME = "DataBase"
MASTER_URL = "mssql+pyodbc://@localhost/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

from sqlalchemy import create_engine, text


def init_database():
    """Функция автоматического создания БД и таблиц"""

    # создавать базы данных внутри обычной транзакции
    master_engine = create_engine(MASTER_URL, isolation_level="AUTOCOMMIT")

    check_query = text(f"SELECT database_id FROM sys.databases WHERE name = '{DB_NAME}'")

    with master_engine.connect() as conn:
        db_exists = conn.scalar(check_query)

        if not db_exists:
            print(f"База данных {DB_NAME} не найдена. Создаю...")
            conn.execute(text(f"CREATE DATABASE [{DB_NAME}]"))
            print(f"База данных {DB_NAME} успешно создана!")
        else:
            print(f"База данных {DB_NAME} уже существует.")

    # Закрываем соединение с master
    master_engine.dispose()

    # Шаг B: Теперь создаем таблицы по вашим моделям в новой базе данных
    Base.metadata.create_all(engine)
    print("Tables successful created")


if __name__ == "__main__":
    init_database()
