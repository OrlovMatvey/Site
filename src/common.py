from fastapi import HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr

from src.config import settings
from src.dependencies import add_auth_context

TEMPLATES = Jinja2Templates(directory=settings.TEMPLATES_DIR, context_processors=[add_auth_context])


class CurrentUserModel(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True


async def auto_set_refresh_cookies(request: Request, call_next) -> Response:
    """Мидлвар для добавления access_token в ответ

    Args:
        request (Request): Тело запроса.
        call_next (_type_): Функция для управления цепочкой событий.

    Returns:
        Response: Тело ответа с access_token внутри.
    """
    response = await call_next(request)
    new_access_token = getattr(request.state, "new_access_token", None)
    if new_access_token:
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*settings.SECONDS_IN_MINUTE
        )
    return response


def auth_exception_handler(request: Request, exc: HTTPException) -> RedirectResponse:
    """Обработчик для исключения с кодом 401

    Args:
        request (Request): Тело запроса
        exc (HTTPException): Исключение

    Returns:
        RedirectResponse: Редирект на страницу регистрации
    """
    return RedirectResponse(url="/Auth/SignUp", status_code=303)


def general_exception_handler(request: Request, exc: HTTPException) -> HTMLResponse:
    """Общий обработчик для исключений

    Args:
        request (Request): Тело запроса.
        exc (HTTPException): Объект исключения.

    Returns:
        HTMLResponse: Шаблон с выводом ошибки.
    """
    context = {"status_code": exc.status_code, "detail": exc.detail}
    return TEMPLATES.TemplateResponse(request=request, name="error.html", context=context)
