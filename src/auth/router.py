"""Модуль эндпоинтов для сервиса Регистрации/Авторизации"""
from fastapi import APIRouter, Cookie, Depends, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.common import TEMPLATES
from src.dependencies import get_db
from src.security import decode_token

from .schemas import LoginModel, RegisterModel
from .service import authenticate_user, create_new_user, delete_refresh_token

router = APIRouter(prefix="/Auth", tags=['AccessControl'])


@router.post("/SignUp")
def register(
    request: RegisterModel = Depends(RegisterModel.formBody),
    db: Session = Depends(get_db)
) -> RedirectResponse:
    """Эндпоинт для регистрации пользователя

    Args:
        request (AuthenticateModel, optional): Тело запроса. Валидация Depends(AuthenticateModel.formBody).
        db (Session, optional): Объект сессии БД. Defaults to Depends(get_db).

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
def login(
    request: LoginModel = Depends(LoginModel.formBody), 
    db: Session = Depends(get_db)
) -> RedirectResponse:
    """Эндпоинт для авторизации пользователя

    Args:
        request (AuthenticateModel): Тело запроса.
        db (Session, optional): Объект сессии БД. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: Редирект на главную страницу.
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
        request (Request): Тело запроса.

    Returns:
        Response: Страница регистрации или редирект на главную страницу.
    """
    access_token = request.cookies.get("access_token")
    if access_token and decode_token(access_token):
        return RedirectResponse(url="/", status_code=303)
    return TEMPLATES.TemplateResponse(request=request, name="user_up.html")


@router.get("/SignIn")
def get_login_page(request: Request) -> Response:
    """Эндпоинт для получения страницы авторизации

    Args:
        request (Request): Тело запроса.

    Returns:
        Response: Страница авторизации или редирект на главную страницу.
    """
    access_token = request.cookies.get("access_token")
    if access_token and decode_token(access_token):
        return RedirectResponse(url="/", status_code=303)
    return TEMPLATES.TemplateResponse(request=request, name="user_in.html")


@router.get("/Logout")
def logout(refresh_token: str = Cookie(None), db: Session = Depends(get_db)) -> RedirectResponse:
    """Эндпоинт для выхода из аккаунта

    Args:
        refresh_token (str, optional): Refresh token из куки. Defaults to Cookie(None).
        db (Session, optional): Объект сессии в бд. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: Редирект на страницу регистрации
    """
    delete_refresh_token(refresh_token, db)
    redirect_response = RedirectResponse(url="/", status_code=303)
    redirect_response.delete_cookie("access_token", path="/")
    redirect_response.delete_cookie("refresh_token", path="/")
    return redirect_response
