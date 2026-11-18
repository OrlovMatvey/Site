"""Модуль бизнес-логики для сервиса Рецептов"""
import base64
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common import CurrentUserModel

from .models import CategoryData, IngredientData, RecipeData, RecipeIngredientData
from .schemas import NewRecipeModel


def get_profile_from_db(
    user_object: CurrentUserModel,
    db: Session
) -> dict[str, Any]:
    """Получение информации из БД для шаблона профиля

    Args:
        user_object (CurrentUserModel): Объект с данными пользователя.
        db (Session): Объект сессии БД.

    Returns:
        dict[str, list]: Словарь с контекстом для шаблона.
    """
    recipes_data: list[dict] = []
    categories_data: list[dict] = []
    ingredients_data: list[dict] = []
    categories_objects = db.scalars(select(CategoryData)).all()
    ingredient_objects = db.scalars(select(IngredientData)).all()
    recipe_objects = db.scalars(
        select(RecipeData).where(RecipeData.user_id == user_object.id)
    ).all()
    for recipe_object in recipe_objects:
        recipe_data = recipe_object.get_dict()
        recipe_data["image"] = base64.b64encode(recipe_object.image).decode("utf-8")
        recipe_data["category"] = recipe_object.category_obj.name
        recipe_data["ingredients"] = {}
        for recipe_ingredient in recipe_object.ingredients:
            recipe_data["ingredients"][recipe_ingredient.ingredient_obj.name] = (
                str(recipe_ingredient.volume)+str(recipe_ingredient.unit)
            )
        recipes_data.append(recipe_data)
    for category in categories_objects:
        categories_data.append({"name": category.name, "id": category.id})
    for ingredient in ingredient_objects:
        ingredients_data.append({"name": ingredient.name, "id": ingredient.id})
    return {
        "categories_data": categories_data, "user_data": user_object,
        "recipes_data": recipes_data, "ingredients_data": ingredients_data
    }


def add_new_recipe(
    user_object: CurrentUserModel,
    recipe_data: NewRecipeModel,
    db: Session
) -> RecipeData:
    """Добавление записи о новом рецепте и его ингредиентах в БД

    Args:
        user_object (CurrentUserModel): Объект с данными пользователя.
        recipe_data (NewRecipeModel): Данные из для записи.
        db (Session): Объект сессии БД.

    Raises:
        HTTPException: Ошибка при создании рецепта

    Returns:
        RecipeData: Объект записи рецепта
    """
    try:
        user_id = user_object.id
        recipe_object = RecipeData(
            title=recipe_data.title,
            category=recipe_data.category,
            body=recipe_data.body,
            image=recipe_data.image,
            user_id=user_id,
        )
        db.add(recipe_object)
        db.flush()
        recipe_id = recipe_object.id
        for ingredient_id, ingredient_vol, ingredient_unit in zip(
            recipe_data.ingredient_ids,
            recipe_data.ingredient_volumes,
            recipe_data.ingredient_units,
            strict=True
        ):
            recipe_ingredient_object = RecipeIngredientData(
                recipe_id=recipe_id,
                ingredient_id=ingredient_id,
                volume=ingredient_vol,
                unit=ingredient_unit
            )
            db.add(recipe_ingredient_object)
        db.commit()
        return recipe_object
    except Exception as e:
        db.rollback()
        print("Произошла ошибка:", e)
        raise HTTPException(
            status_code=500, detail="Ошибка при создании рецепта"
        )


def get_recipes_from_db(db: Session) -> dict[str, list]:
    """Получение информации из БД для шаблона главной страницы

    Args:
        db (Session): Объект сессии БД.

    Returns:
        dict[str, list]: Словарь с контекстом для шаблона.
    """
    recipes_data: list[dict] = []
    recipe_objects = db.scalars(select(RecipeData)).all()
    for recipe_object in recipe_objects:
        recipe_data = recipe_object.get_dict()
        recipe_data["image"] = base64.b64encode(
            recipe_data["image"]
        ).decode("utf-8")
        recipe_data["category"] = recipe_object.category_obj.name
        recipes_data.append(recipe_data)
    return {"recipes_data": recipes_data}
