"""Модуль Pydantic схем для сервиса Рецептов"""
from typing import Self

from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class NewRecipeModel(BaseModel):
    """Pydantic-модель для валидации запроса на создание нового рецепта

    Args:
        BaseModel (_type_): Базовый класс для Pydantic-моделей

    Returns:
        _type_: Экземпляр модели
    """
    title: str
    category: int
    body: str
    ingredient_ids: list[int]
    ingredient_volumes: list[float]
    ingredient_units: list[str]
    image: bytes

    @classmethod
    async def formBody(
        cls,
        title: str = Form(...),
        category: int = Form(...),
        body: str = Form(...),
        ingredient_ids: list[int] = Form(...),
        ingredient_volumes: list[float] = Form(...),
        ingredient_units: list[str] = Form(...),
        image: UploadFile = File(...)
    ) -> Self:
        image_bytes = await image.read()
        return cls(
            title=title,
            category=category,
            body=body,
            ingredient_ids=ingredient_ids,
            ingredient_volumes=ingredient_volumes,
            ingredient_units=ingredient_units,
            image=image_bytes
        )
