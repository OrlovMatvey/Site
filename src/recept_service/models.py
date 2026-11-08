"""Модуль ORM-моделей БД для сервиса Рецептов"""
from sqlalchemy import JSON, Float, ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class RecipeData(Base):
    """Модель для таблицы с рецептами"""
    __tablename__ = "RecipeData"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    category: Mapped[int] = mapped_column(ForeignKey('CategoryData.id'))
    body: Mapped[dict] = mapped_column(JSON, default=dict)
    image: Mapped[bytes] = mapped_column(LargeBinary)
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
    count_likes: Mapped[int] = mapped_column(nullable=True)
    count_dislikes: Mapped[int] = mapped_column(nullable=True)


class CommentData(Base):
    """Модель для таблицы с комментариями"""
    __tablename__ = "CommentData"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(1000))
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
    recipe_id: Mapped[int] = mapped_column(ForeignKey('RecipeData.id'))


class FavoriteRecipeData(Base):
    """Модель для таблицы с избранными рецептами"""
    __tablename__ = "FavoriteRecipeData"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
    recipe_id: Mapped[int] = mapped_column(ForeignKey('RecipeData.id'))


class IngredientData(Base):
    """Модель для таблицы с ингредиентами"""
    __tablename__ = "IngredientData"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(50))


class CategoryData(Base):
    """Модель для таблицы с категориями"""
    __tablename__ = "CategoryData"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(50))


class RecipeIngredientData(Base):
    """Модель для таблицы с ингредиентами рецептов"""
    __tablename__ = "RecipeIngredientData"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('RecipeData.id'))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('IngredientData.id'))
    volume: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(20))
