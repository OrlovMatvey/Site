"""Модуль создания таблиц в БД"""
from src.auth import UserData, UserTokenData
from src.database import Base, engine
from src.recept_service import (
    CategoryData,
    CommentData,
    FavoriteReceptData,
    IngredientData,
    ReceptData,
)


def create_db() -> None:
    """Создание и обновление БД"""
    Base.metadata.create_all(engine)
    print("Tables successful created")


if __name__ == "__main__":
    create_db()
