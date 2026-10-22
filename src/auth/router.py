"""Модуль эндпоинтов для сервиса Регистрации/Авторизации"""
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.config import settings
from src.dependencies import get_db, is_authenticated
from src.security import decode_token

from .schemas import AuthenticateModel
from .service import authenticate_user, create_new_user

router = APIRouter(prefix="/Auth", tags=['AccessControl'])


@router.post("/SignUp")
def register(request: AuthenticateModel = Depends(AuthenticateModel.formBody),
             db: Session = Depends(get_db)) -> RedirectResponse:
    """Эндпоинт для регистрации пользователя

    Args:
        response (Response): Тело ответа
        request (AuthenticateModel, optional): Тело запроса. Валидация Depends(AuthenticateModel.formBody).
        db (Session, optional): Открытие сессии в БД. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: Редирект на главную страницу
    """
    coockie_data: dict = create_new_user(
        request.username, request.email, request.password, db
    )
    redirect_response = RedirectResponse(url="/", status_code=303)
    redirect_response.set_cookie(
        key="access_token",
        value=coockie_data["access_token"],
        httponly=True,
        max_age=coockie_data["access_expires_in"]
    )
    redirect_response.set_cookie(
        key="refresh_token",
        value=coockie_data["refresh_token"],
        httponly=True,
        max_age=coockie_data["refresh_expires_in"]
    )
    return redirect_response


@router.post("/SignIn")
def login(request: AuthenticateModel, 
          response: Response, 
          db: Session = Depends(get_db)) -> RedirectResponse:
    """Эндпоинт для авторизации пользователя

    Args:
        request (AuthenticateModel): Тело запроса
        response (Response): Тело ответа
        db (Session, optional): Открытие сессии в БД. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: Редирект на главную страницу
    """
    coockie_data = authenticate_user(request.email, request.password, db)
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


@router.get("/SignUp")
def get_register_page(request: Request) -> Response:
    """Эндпоинт для получения страницы регистрации

    Args:
        request (Request): Тело запроса

    Returns:
        HTMLResponse: Страница регистрации
    """
    access_token = request.cookies.get("access_token")
    if access_token and decode_token(access_token):
        return RedirectResponse(url="/", status_code=303)
    return settings.TEMPLATES.TemplateResponse(request=request, name="user_up.html")


@router.get("/SignIn")
def get_login_page(request: Request) -> Response:
    """Эндпоинт для получения страницы авторизации

    Args:
        request (Request): Тело запроса

    Returns:
        HTMLResponse: Страница авторизации
    """
    access_token = request.cookies.get("access_token")
    if access_token and decode_token(access_token):
        return RedirectResponse(url="/", status_code=303)
    return settings.TEMPLATES.TemplateResponse(request=request, name="user_in.html")
