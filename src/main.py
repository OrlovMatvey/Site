"""Главный модуль запуска приложения"""
from pathlib import Path

import uvicorn
from fastapi import Cookie, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.auth import auth_router
from src.recept_service import service_router

app = FastAPI()

BASE_DIR = Path(__file__).absolute().parent

app.mount("/static", StaticFiles(directory=BASE_DIR/"static"))
app.include_router(auth_router)
app.include_router(service_router)


@app.get("/")
def main(request: Request, refresh_token: str = Cookie(None)) -> RedirectResponse:
    """Точка входа в приложение

    Args:
        request (Request): Тело запроса
        refresh_token (str, optional): Refresh токен из куки

    Returns:
        RedirectResponse: Редирект на другую страницу
    """
    if refresh_token:
        return RedirectResponse(url="/Service/Main", status_code=303)
    else:
        return RedirectResponse(url="/Auth/UserUp", status_code=303)


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
