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
    "User": UserData,
    "UserToken": UserTokenData,
    "Recipe": RecipeData,
    "Ingredient": IngredientData,
    "RecipeIngredient": RecipeIngredientData,
    "FavoriteRecipe": FavoriteRecipeData,
    "Category": CategoryData,
    "Comment": CommentData
}


def get_table_data_from_db(table_name: str, db: Session) -> dict[str, list]:
    record_dicts: list[dict] = []
    table_model = TABLES_MAP.get(table_name)
    if not table_model:
        return {"fields": [], "records": []}
    table_fields = table_model.get_table_fields()
    record_objects = db.scalars(select(table_model)).all()
    for record_oject in record_objects:
        record_dicts.append(record_oject.get_dict())
    return {"fields": table_fields, "records": record_dicts}


def delete_record_by_id(table_name: str, record_id: int, db: Session) -> bool:
    table_model = TABLES_MAP.get(table_name)
    if not table_model:
        return False
    record_object = db.scalar(select(table_model).where(table_model.id == record_id))
    if not record_object:
        return False
    db.delete(record_object)
    db.commit()
    return True


def update_record_by_id(table_name: str, record_id: int, db: Session) -> bool:
    pass
    # Сделать функционал обновления записи
