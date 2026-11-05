from typing import Self

from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class RecipeModel(BaseModel):
    title: str
    category: int
    body: str
    ingredient_name: list[str]
    ingredient_volume: list[float]
    ingredient_unit: list[str]
    image: bytes

    @classmethod
    async def formBody(
        cls,
        title: str = Form(...),
        category: int = Form(...),
        body: str = Form(...),
        ingredient_name: list[str] = Form(...),
        ingredient_volume: list[float] = Form(...),
        ingredient_unit: list[str] = Form(...),
        image: UploadFile = File(...)
    ) -> Self:
        image_bytes = await image.read()
        return cls(
            title=title,
            category=category,
            body=body,
            ingredient_name=ingredient_name,
            ingredient_volume=ingredient_volume,
            ingredient_unit=ingredient_unit,
            image=image_bytes
        )
