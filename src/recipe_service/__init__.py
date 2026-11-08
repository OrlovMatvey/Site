"""Модуль инициализации пакета для сервиса Рецептов"""
from .models import (
    CategoryData,
    CommentData,
    FavoriteRecipeData,
    IngredientData,
    RecipeData,
    RecipeIngredientData,
)
from .router import router as service_router

__all__ = [
    "CategoryData",
    "CommentData",
    "FavoriteRecipeData",
    "IngredientData",
    "RecipeData",
    "RecipeIngredientData",
    "service_router"
]
