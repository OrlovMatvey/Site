"""Модуль ORM-моделей БД для сервиса Рецептов"""
from datetime import datetime

from sqlalchemy import Float, ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class RecipeData(Base):
    """Модель для таблицы с рецептами"""
    __tablename__ = "RecipeData"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    category: Mapped[int] = mapped_column(ForeignKey('CategoryData.id'))
    body: Mapped[str] = mapped_column(String(3000))
    image: Mapped[bytes] = mapped_column(LargeBinary)
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
    count_likes: Mapped[int] = mapped_column(nullable=True)
    count_dislikes: Mapped[int] = mapped_column(nullable=True)

    ingredients: Mapped[list["RecipeIngredientData"]] = relationship(
        "RecipeIngredientData",
        back_populates="recipe_obj",
        cascade="all, delete-orphan"
    )

    category_obj: Mapped["CategoryData"] = relationship("CategoryData", lazy="joined")

    # Можно добавить поля с фильтрацией, сортировкой и стратегией загрузки с
    # помощью relationship


class CommentData(Base):
    """Модель для таблицы с комментариями"""
    __tablename__ = "CommentData"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(1000))
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
    recipe_id: Mapped[int] = mapped_column(ForeignKey('RecipeData.id'))
    created_at: Mapped[datetime] = mapped_column()


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

    recipes: Mapped[list["RecipeIngredientData"]] = relationship(
        "RecipeIngredientData",
        cascade="all, delete-orphan"
    )


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

    recipe_obj: Mapped["RecipeData"] = relationship(back_populates="ingredients")
    ingredient_obj: Mapped["IngredientData"] = relationship("IngredientData", lazy="joined")

class RecipeReactionData(Base):
    __tablename__ = "RecipeReactionData"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("RecipeData.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("UserData.id"))
    is_like: Mapped[bool] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()