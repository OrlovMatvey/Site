"""Модуль эндпоинтов для сервиса Рецептов"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.common import TEMPLATES, CurrentUserModel
from src.dependencies import get_current_user, get_db

from .schemas import NewRecipeModel
from .service import add_new_recipe, get_profile_from_db, get_recipes_from_db

router = APIRouter(prefix="/Service", tags=["BusinessProcess"])


@router.get("/Main")
def get_index_page(
    request: Request,
    current_user: CurrentUserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> HTMLResponse:
    """Эндпоинт для получения главной страницы

    Args:
        request (Request): Тело запроса.
        current_user (CurrentUserModel, optional): Текущий юзер из зависимости.
        db (Session, optional): Объект сессии БД.
    Returns:
        HTMLResponse: Возвращает шаблон главной страницы
    """
    context = get_recipes_from_db(db)
    return TEMPLATES.TemplateResponse(
        request=request, name="index.html", context=context
    )


@router.get("/Profile")
def get_profile_page(
    request: Request,
    current_user: CurrentUserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> HTMLResponse:
    """Эндпоинт для получения страницы профиля

    Args:
        request (Request): Тело запроса.
        current_user (CurrentUserModel, optional): Текущий юзер из зависимости.
        db (Session, optional): Объект сессии БД.

    Returns:
        HTMLResponse: Возвращает шаблон страницы профиля
    """
    context = get_profile_from_db(current_user, db)
    return TEMPLATES.TemplateResponse(
        request=request, name="profile.html", context=context
    )


@router.post("/Profile")
def create_recipe(
    recipe_data: NewRecipeModel = Depends(NewRecipeModel.formBody),
    current_user: CurrentUserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> RedirectResponse:
    """Эндпоинт для создания нового рецепта

    Args:
        recipe_data (NewRecipeModel, optional): Данные из формы.
        current_user (CurrentUserModel, optional): Текущий юзер из зависимости.
        db (Session, optional): Объект сессии БД.

    Returns:
        RedirectResponse: Перезагрузка страницы(Редирект)
    """
    add_new_recipe(
        current_user,
        recipe_data.title, recipe_data.category,
        recipe_data.body, recipe_data.ingredient_ids,
        recipe_data.ingredient_volumes, recipe_data.ingredient_units,
        recipe_data.image, db
        )
    return RedirectResponse(url="/Service/Profile", status_code=303)
