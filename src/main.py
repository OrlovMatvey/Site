"""Главный модуль запуска приложения"""
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteException

from src.admin import admin_router
from src.auth import auth_router
from src.common import (
    auth_exception_handler,
    auto_set_refresh_cookies,
    general_exception_handler,
)
from src.config import settings
from src.dependencies import is_authenticated
from src.recipe_service import service_router

app = FastAPI()

app.add_exception_handler(StarletteException, general_exception_handler)
app.add_exception_handler(401, auth_exception_handler)
app.middleware("http")(auto_set_refresh_cookies)
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
app.include_router(auth_router)
app.include_router(service_router)
app.include_router(admin_router)


@app.get("/", dependencies=[Depends(is_authenticated)])
def main() -> RedirectResponse:
    """Точка входа в приложение

    Returns:
        RedirectResponse: Редирект на главную страницу
    """
    return RedirectResponse(url="/Service/Main", status_code=303)


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
