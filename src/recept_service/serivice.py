from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
import base64

from src.auth import UserData
from src.security import decode_token

from .models import CategoryData, IngredientData, RecipeData, RecipeIngredientData


def get_profile_from_db(access_token: str, db: Session):
    user_data: dict[str, str] = {}
    recipes_data: list[dict] = []
    categories_data: list[dict] = []
    ingredients_data: list[dict] = []
    context: dict[list] = {}
    token_data = decode_token(access_token)
    user_data = db.scalar(select(UserData).where(UserData.id == token_data["sub"]))
    user_data = user_data.get_dict()
    categories = db.scalars(select(CategoryData)).all()
    ingredients = db.scalars(select(IngredientData)).all()
    recipes = db.scalars(select(RecipeData).where(RecipeData.user_id == token_data["sub"])).all()
    if not recipes:
        recipes_data.append("Вы еще не добавили свои рецепты!")
    else:
        for recipe in recipes:
            recipe.image = base64.b64encode(recipe.image).decode("utf-8")
            recipes_data.append(recipe.get_dict())
    for category in categories:
        categories_data.append({"name": category.name, "id": category.id})
    for ingredient in ingredients:
        ingredients_data.append({"name": ingredient.name, "id": ingredient.id})
    context["categories_data"] = categories_data
    context["user_data"] = [user_data]
    context["recipes_data"] = recipes_data
    context["ingredients_data"] = ingredients_data
    print(ingredients_data)
    return context


def add_new_recipe(
        access_token: str, title: str, category: int, body: str,
        ingredient_ids: list[int], ingredient_volumes: list[float],
        ingredient_units: list[str], image: bytes, db: Session
        ):
    token_data = decode_token(access_token)
    user_id = token_data["sub"]
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
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при создании рецепта")


def get_recipes_from_db(db: Session):
    context: dict[list] = {}
    recipes_data: list[dict] = []
    recipes = db.scalars(select(RecipeData)).all()
    for recipe in recipes:
        recipe.image = base64.b64encode(recipe.image).decode("utf-8")
        recipes_data.append(recipe.get_dict())
    context["recipes_data"] = recipes_data
    return context
