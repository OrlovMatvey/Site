"""Модуль эндпоинтов для сервиса Рецептов"""
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.auth import UserData
from src.config import settings
from src.dependencies import get_current_user, get_db

from .schemas import RecipeModel
from .service import add_new_recipe, get_profile_from_db, get_recipes_from_db

router = APIRouter(prefix="/Service", tags=["BusinessProcess"])


@router.get("/Main")
def get_index_page(
    request: Request,
    current_user: UserData = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> HTMLResponse:
    """Эндпоинт для получения главной страницы

    Args:
        request (Request): Тело запроса
        current_user (UserData, optional): Текущий юзер из зависимости. Defaults to Depends(get_current_user).
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
    current_user: UserData = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> HTMLResponse:
    """Эндпоинт для получения страницы профиля

    Args:
        request (Request): Тело запроса
        current_user (UserData, optional): Текущий юзер из зависимости. Defaults to Depends(get_current_user).
        db (Session, optional): Объект сессии БД.. Defaults to Depends(get_db).

    Returns:
        HTMLResponse: Возвращает шаблон страницы профиля
    """
    context = get_profile_from_db(current_user, db)
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="profile.html", context=context
    )


@router.post("/Profile")
def create_recipe(
    recipe_data: RecipeModel = Depends(RecipeModel.formBody),
    current_user: UserData = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Response:
    """Эндпоинт для создания нового рецепта

    Args:
        recipe_data (RecipeModel, optional): Данные из формы. Defaults to Depends(RecipeModel.formBody).
        current_user (UserData, optional): Текущий юзер из зависимости. Defaults to Depends(get_current_user).
        db (Session, optional): Объект сессии БД.. Defaults to Depends(get_db).

    Returns:
        Response: Пустой ответ 204
    """
    add_new_recipe(
        current_user,
        recipe_data.title, recipe_data.category,
        recipe_data.body, recipe_data.ingredient_ids,
        recipe_data.ingredient_volumes, recipe_data.ingredient_units,
        recipe_data.image, db
        )
    return RedirectResponse(url="/Service/Profile", status_code=303)
