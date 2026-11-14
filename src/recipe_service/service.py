"""Модуль бизнес-логики для сервиса Рецептов"""
import base64

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common import CurrentUserModel

from .models import CategoryData, IngredientData, RecipeData, RecipeIngredientData
from .schemas import NewRecipeModel


def get_profile_from_db(
    user_object: CurrentUserModel,
    db: Session
) -> dict[str, list]:
    """Получение информации из БД для шаблона профиля

    Args:
        user_object (CurrentUserModel): Объект с данными пользователя.
        db (Session): Объект сессии БД.

    Returns:
        dict[str, list]: Словарь с контекстом для шаблона.
    """
    context: dict[str, list] = {}
    recipes_data: list[dict] = []
    categories_data: list[dict] = []
    ingredients_data: list[dict] = []
    categories = db.scalars(select(CategoryData)).all()
    ingredients = db.scalars(select(IngredientData)).all()
    recipes = db.scalars(
        select(RecipeData).where(RecipeData.user_id == user_object.id)
    ).all()
    for recipe in recipes:
        recipe.image = base64.b64encode(recipe.image).decode("utf-8")
        recipes_data.append(recipe.get_dict())
    for category in categories:
        categories_data.append({"name": category.name, "id": category.id})
    for ingredient in ingredients:
        ingredients_data.append({"name": ingredient.name, "id": ingredient.id})
    context["categories_data"] = categories_data
    context["user_data"] = [user_object]
    context["recipes_data"] = recipes_data
    context["ingredients_data"] = ingredients_data
    return context


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
    user_id = user_object.id
    try:
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
            recipe_data.ingredient_units
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
    except Exception:
        db.rollback()
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
        recipes_data.append(recipe_data)
    return {"recipes_data": recipes_data}
