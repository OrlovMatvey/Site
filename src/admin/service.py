"""Модуль бизнес-логики для сервиса Администрации"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth import UserData, UserTokenData
from src.exceptions import NotFoundError
from src.recipe_service import (
    CategoryData,
    CommentData,
    FavoriteRecipeData,
    IngredientData,
    RecipeData,
    RecipeIngredientData,
    RecipeReactionData,
)

TABLES_MAP = {
    "User": UserData,
    "UserToken": UserTokenData,
    "Recipe": RecipeData,
    "Ingredient": IngredientData,
    "RecipeIngredient": RecipeIngredientData,
    "FavoriteRecipe": FavoriteRecipeData,
    "RecipeReaction": RecipeReactionData,
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


def delete_record_by_id(table_name: str, record_id: int, db: Session) -> None:
    table_model = TABLES_MAP.get(table_name)
    if not table_model:
        raise NotFoundError(detail="Таблица не найдена")
    record_object = db.scalar(
        select(table_model).where(table_model.id == record_id)
    )
    if not record_object:
        raise NotFoundError(detail="Запись не найдена")
    db.delete(record_object)
    db.commit()


# Переделать логику обновления
def update_record_by_id(
    table_name: str,
    record_id: int,
    record_data: dict,
    db: Session
) -> None:
    table_model = TABLES_MAP.get(table_name)
    if not table_model:
        raise NotFoundError(detail="Таблица не найдена")
    record_object = db.scalar(
        select(table_model).where(table_model.id == record_id)
    )
    if not record_object:
        raise NotFoundError(detail="Запись не найдена")
    model_fields = table_model.get_table_fields()
    for model_field in model_fields:
        if model_field != "id" and model_field != "image":
            setattr(record_object, model_field, record_data[model_field])
    db.add(record_object)
    db.commit()


def add_new_record(
    table_name: str,
    record_data: dict,
    db: Session
) -> None:
    table_model = TABLES_MAP.get(table_name)
    if not table_model:
        raise NotFoundError(detail="Таблица не найдена")
    record_object = table_model()
    model_fields = table_model.get_table_fields()
    for model_field in model_fields:
        if model_field != "id":
            setattr(record_object, model_field, record_data[model_field])
    db.add(record_object)
    db.commit()
