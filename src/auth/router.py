"""Модуль эндпоинтов для сервиса Регистрации/Авторизации"""
from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db

from .schemas import AuthenticateModel
from .service import auth_user, new_user

router = APIRouter(prefix="/Auth", tags=['AccessControl'])


@router.post("/UserUp")
def up_user(request: AuthenticateModel = Depends(AuthenticateModel.formBody), db: Session = Depends(get_db)) -> RedirectResponse:
    """Эндпоинт для регистрации пользователя

    Args:
        response (Response): Тело ответа
        request (AuthenticateModel, optional): Тело запроса. Валидация Depends(AuthenticateModel.formBody).
        db (Session, optional): Открытие сессии в БД. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: _description_
    """
    coockie_data = new_user(
        request.username, request.email, request.password, db
    )
    redirect_response = RedirectResponse(url="/", status_code=303)
    redirect_response.set_cookie(
        key="access_token",
        value=coockie_data["access_token"],
        domain="http://127.0.0.1:8000",
        max_age=coockie_data["access_expires_in"]
    )
    redirect_response.set_cookie(
        key="refresh_token",
        value=coockie_data["refresh_token"],
        domain="http://127.0.0.1:8000",
        max_age=coockie_data["refresh_expires_in"]
    )
    return redirect_response


@router.post("/UserIn")
def in_user(request: AuthenticateModel, response: Response, db: Session = Depends(get_db)) -> RedirectResponse:
    """Эндпоинт для авторизации пользователя

    Args:
        request (AuthenticateModel): Тело запроса
        response (Response): Тело ответа
        db (Session, optional): Открытие сессии в БД. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: Редирект на главную страницу
    """
    coockie_data = auth_user(request.email, request.password, db)
    redirect_response = RedirectResponse(url="/", status_code=303)
    redirect_response.set_cookie(
        key="access_token",
        value=coockie_data["access_token"],
        max_age=coockie_data["access_expires_in"]
    )
    redirect_response.set_cookie(
        key="refresh_token",
        value=coockie_data["refresh_token"],
        max_age=coockie_data["refresh_expires_in"]
    )
    return redirect_response
