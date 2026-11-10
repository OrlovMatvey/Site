"""Модуль бизнес-логики для сервиса Администрации"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth import UserData, UserTokenData
from src.recipe_service import (
    CategoryData,
    CommentData,
    FavoriteRecipeData,
    IngredientData,
    RecipeData,
    RecipeIngredientData,
)

TABLES_MAP = {
    "users": UserData,
    "tokens": UserTokenData,
    "recipes": RecipeData,
    "ingredients": IngredientData,
    "recipe_ingredients": RecipeIngredientData,
    "favorites": FavoriteRecipeData,
    "categories": CategoryData,
    "comments": CommentData
}


def get_admin_dashboard_data(db: Session, table_name: str) -> dict:
    """Динамически извлекает поля и строки для любой таблицы БД"""
    model = TABLES_MAP.get(table_name)

    if not model:
        return {"fields": [], "rows": [], "verbose_name": "Неизвестная таблица"}

    # Интимная магия: используем ваши методы из класса Base!
    fields = model.get_table_fields()
    rows = db.scalars(select(model)).all()

    # Человеческое название для заголовка на странице
    verbose_names = {
        "users": "Пользователи",
        "tokens": "Токены пользователей",
        "recipes": "Рецепты",
        "ingredients": "Ингредиенты",
    }

    return {
        "fields": fields,
        "rows": rows,
        "verbose_name": verbose_names.get(table_name, table_name.capitalize())
    }


def delete_row_by_id(db: Session, table_name: str, row_id: int) -> bool:
    """Удаляет запись по ID из выбранной таблицы с использованием db.scalar"""
    print(111)
    model = TABLES_MAP.get(table_name)
    if not model:
        print(123)
        return False

    # Формируем явный SQL-запрос выборки по первичному ключу ID
    stmt = select(model).where(model.id == row_id)

    # Получаем объект через db.scalar
    obj = db.scalar(stmt)
    if not obj:
        print(321)
        return False

    db.delete(obj)
    db.commit()
    return True


def update_row_by_id(db: Session, table_name: str, row_id: int, data: dict) -> bool:
    """Динамически обновляет запись с использованием db.scalar и select"""
    model = TABLES_MAP.get(table_name)
    if not model:
        return False

    # Формируем SQL-запрос выборки объекта для изменения
    stmt = select(model).where(model.id == row_id)

    # Извлекаем объект из базы данных
    obj = db.scalar(stmt)
    if not obj:
        return False

    # Динамически обновляем атрибуты модели на основе пришедшего JSON
    for key, value in data.items():
        if key != "id" and hasattr(obj, key):
            # Проверяем, если значение является строкой, но само поле в БД — булевое
            # (или если мы просто хотим безопасно распарсить "True"/"Да")
            if isinstance(value, str):
                cleaned_value = value.strip().lower()
                if cleaned_value in ("true", "да", "1"):
                    value = True
                elif cleaned_value in ("false", "нет", "0"):
                    value = False
            setattr(obj, key, value)

    db.commit()
    return True
