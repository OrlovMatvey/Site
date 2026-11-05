from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth import UserData
from src.security import decode_token

from .models import IngredientData, RecipeData, CategoryData


def get_profile_from_db(access_token: str, db: Session):
    user_data: dict[str, str] = {}
    recepts_data: list[dict] = []
    categories_data: list[dict] = []
    ingredients_data: list[str] = []
    context: dict[list] = {}
    token_data = decode_token(access_token)
    user_data = db.scalar(select(UserData).where(UserData.id == token_data["sub"]))
    user_data = user_data.get_dict()
    categories = db.scalars(select(CategoryData)).all()
    ingredients = db.scalars(select(IngredientData)).all()
    """ recepts = db.scalars(select(RecipeData).where(RecipeData.user_id == token_data["sub"])).all()
    if not recepts:
        recepts_data.append("Вы еще не добавили свои рецепты!")
    else:
        for recept in recepts:
            recepts_data.append(recept.get_dict())
    """
    for category in categories:
        categories_data.append({"name": category.name, "id": category.id})
    for ingredient in ingredients:
        ingredients_data.append(ingredient.name)
    context["categories_data"] = categories_data
    context["user_data"] = [user_data]
    context["recepts_data"] = recepts_data
    context["ingredients_data"] = ingredients_data
    print(ingredients_data)
    return context


def add_new_recipe(
        access_token: str, title: str, category: int, body: str,
        ingredient_name: list[str], ingredient_volume: list[float],
        ingredient_unit: list[str], image: bytes, db: Session
        ):
    # token_data = decode_token(access_token)
    # user_id = token_data["sub"]
    recipe_object = RecipeData(
        title=title,
        category=category,
        body=body,
        image=image
    )
    db.add(recipe_object)
    db.commit
