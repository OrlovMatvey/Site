"""Модуль эндпоинтов для сервиса Рецептов"""
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.config import settings
from src.dependencies import get_db, is_authenticated

from .schemas import RecipeModel
from .service import add_new_recipe, get_profile_from_db, get_recipes_from_db

router = APIRouter(prefix="/Service", tags=["BusinessProcess"])


@router.get("/Main")
def get_index_page(
    request: Request,
    access_token: bool = Depends(is_authenticated),
    db: Session = Depends(get_db)
) -> HTMLResponse:
    """Эндпоинт для получения главной страницы

    Args:
        request (Request): Тело запроса
        access_token (bool, optional): Access_token из зависимости. Defaults to Depends(is_authenticated).
        db (Session, optional): Объект сессии БД. Defaults to Depends(get_db).

    Returns:
        HTMLResponse: Возвращает шаблон главной страницы
    """
    context = get_recipes_from_db(db)
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="index.html", context=context
    )


@router.get("/Profile")
def get_profile_page(
    request: Request,
    access_token: bool = Depends(is_authenticated),
    db: Session = Depends(get_db)
) -> HTMLResponse:
    """Эндпоинт для получения страницы профиля

    Args:
        request (Request): Тело запроса
        access_token (bool, optional): Access_token из зависимости. Defaults to Depends(is_authenticated).
        db (Session, optional): Объект сессии БД.. Defaults to Depends(get_db).

    Returns:
        HTMLResponse: Возвращает шаблон страницы профиля
    """
    context = get_profile_from_db(access_token, db)
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="profile.html", context=context
    )

# Надо сделать админ-панель
@router.get("/Admin")
def get_admin_page(
    request: Request,
    access_token: bool = Depends(is_authenticated)
) -> HTMLResponse:
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="admin.html"
    )


@router.post("/Profile")
def create_recipe(
    recipe_data: RecipeModel = Depends(RecipeModel.formBody),
    access_token: bool = Depends(is_authenticated),
    db: Session = Depends(get_db)
) -> Response:
    """Эндпоинт для создания нового рецепта

    Args:
        recipe_data (RecipeModel, optional): Данные из формы. Defaults to Depends(RecipeModel.formBody).
        access_token (bool, optional): Access_token из зависимости. Defaults to Depends(is_authenticated).
        db (Session, optional): Объект сессии БД.. Defaults to Depends(get_db).

    Returns:
        Response: Пустой ответ 204
    """
    add_new_recipe(
        access_token,
        recipe_data.title, recipe_data.category,
        recipe_data.body, recipe_data.ingredient_ids,
        recipe_data.ingredient_volumes, recipe_data.ingredient_units,
        recipe_data.image, db
        )
    return Response(status_code=204)
