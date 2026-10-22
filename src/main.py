"""Главный модуль запуска приложения"""
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.auth import auth_router
from src.config import settings
from src.dependencies import is_authenticated
from src.recept_service import service_router

app = FastAPI()

BASE_DIR = Path(__file__).absolute().parent


@app.middleware("http")
async def auto_set_refresh_cookies(request: Request, call_next):
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


@app.exception_handler(401)
async def auth_exception_handler(request: Request, exc: HTTPException) -> RedirectResponse:
    """Обработчик для исключения с кодом 401

    Args:
        request (Request): Тело запроса
        exc (HTTPException): Исключение

    Returns:
        RedirectResponse: Редирект на страницу регистрации
    """
    return RedirectResponse(url="/Auth/SignUp", status_code=303)

app.mount("/static", StaticFiles(directory=BASE_DIR/"static"))
app.include_router(auth_router)
app.include_router(service_router)


@app.get("/")
def main(request: Request, authenticated: bool = Depends(is_authenticated)) -> RedirectResponse:
    """Точка входа в приложение

    Args:
        request (Request): Тело запроса

    Returns:
        RedirectResponse: Редирект на главную страницу
    """
    return RedirectResponse(url="/Service/Main", status_code=303)


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
