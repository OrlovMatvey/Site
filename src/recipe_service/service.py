"""Модуль бизнес-логики для сервиса Рецептов"""
import base64

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common import CurrentUserModel

from .models import CategoryData, IngredientData, RecipeData, RecipeIngredientData


def get_profile_from_db(user_object: CurrentUserModel, db: Session) -> dict[str, list]:
    """Получение информации из БД для шаблона профиля

    Args:
        access_token (str): Access_token.
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
    recipes = db.scalars(select(RecipeData).where(RecipeData.user_id == user_object.id)).all()
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
    user_object: CurrentUserModel, title: str, category: int, body: str,
    ingredient_ids: list[int], ingredient_volumes: list[float],
    ingredient_units: list[str], image: bytes, db: Session
) -> RecipeData:
    """Добавление записи о новом рецепте и его ингредиентах в БД

    Args:
        access_token (str): Access_token.
        title (str): Заголовок рецепта.
        category (int): Категория рецепта.
        body (str): Основной текст рецепта.
        ingredient_ids (list[int]): ID всех ингредиентов.
        ingredient_volumes (list[float]): Значения всех ингредиентов.
        ingredient_units (list[str]): Величины всех ингредиентов.
        image (bytes): Изображение рецепта.
        db (Session): Объект сессии БД.

    Raises:
        HTTPException: Ошибка при создании рецепта

    Returns:
        RecipeData: Объект записи рецепта
    """
    user_id = user_object.id
    try:
        recipe_object = RecipeData(
            title=title,
            category=category,
            body=body,
            image=image,
            user_id=user_id,
        )
        db.add(recipe_object)
        db.flush()
        recipe_id = recipe_object.id
        for ing_id, ing_vol, ing_unit in zip(ingredient_ids, ingredient_volumes, ingredient_units):
            recipe_ingredient_object = RecipeIngredientData(
                recipe_id=recipe_id,
                ingredient_id=ing_id,
                volume=ing_vol,
                unit=ing_unit
            )
            db.add(recipe_ingredient_object)
        db.commit()
        return recipe_object
    # Нужно переделать обработку исключения
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при создании рецепта")


def get_recipes_from_db(db: Session) -> dict[str, list]:
    """Получение информации из БД для шаблона главной страницы

    Args:
        db (Session): Объект сессии БД.

    Returns:
        dict[str, list]: Словарь с контекстом для шаблона.
    """
    context: dict[str, list] = {}
    recipes_data: list[dict] = []
    recipes = db.scalars(select(RecipeData)).all()
    for recipe in recipes:
        recipe.image = base64.b64encode(recipe.image).decode("utf-8")
        recipes_data.append(recipe.get_dict())
    context["recipes_data"] = recipes_data
    return context
