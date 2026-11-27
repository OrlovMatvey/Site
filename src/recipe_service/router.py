"""Модуль эндпоинтов для сервиса Рецептов"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlalchemy.orm import Session

from src.common import TEMPLATES, CurrentUserModel
from src.dependencies import get_current_user, get_db

from .schemas import NewRecipeModel
from .service import (
    add_new_comment_for_recipe,
    add_new_reaction_for_recipe,
    add_new_recipe,
    export_recipe_for_user,
    get_profile_from_db,
    get_recipes_from_db,
)

router = APIRouter(prefix="/Service", tags=["BusinessProcess"])


@router.get("/Main", dependencies=[Depends(get_current_user)])
def get_index_page(
    request: Request,
    db: Session = Depends(get_db)
) -> HTMLResponse:
    """Эндпоинт для получения главной страницы

    Args:
        request (Request): Тело запроса.
        db (Session, optional): Объект сессии БД.
    Returns:
        HTMLResponse: Возвращает шаблон главной страницы.
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
        HTMLResponse: Возвращает шаблон страницы профиля.
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
        RedirectResponse: Перезагрузка страницы(Редирект).
    """
    add_new_recipe(current_user, recipe_data, db)
    return RedirectResponse(url="/Service/Profile", status_code=303)


# Функционал добавления реакции Лайк/Дизлайк
@router.post("/Reaction/{recipe_id}")
async def add_reaction(
    request: Request,
    recipe_id: int,
    current_user: CurrentUserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Response:
    reaction_data = await request.json()
    add_new_reaction_for_recipe(current_user, recipe_id, reaction_data, db)
    return Response(status_code=200)


# Функционал добавления комментария
@router.post("/Comment/{recipe_id}")
async def add_comment(
    request: Request,
    recipe_id: int,
    current_user: CurrentUserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Response:
    comment_data = await request.json()
    add_new_comment_for_recipe(current_user, recipe_id, comment_data, db)
    return Response(status_code=200)


@router.get("/Export/{recipe_id}")
def export_recipe(recipe_id: int, db: Session = Depends(get_db)) -> Response:
    pdf_bytes = export_recipe_for_user(recipe_id, db)
    return Response(
        status_code=200,
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=recipe_{recipe_id}.pdf"
        }
    )
