"""Главный модуль запуска приложения"""
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.auth import auth_router

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR/"static"))
app.include_router(auth_router)


@app.get("/as")
def index() -> FileResponse:
    """Точка входа

    Returns:
        FileResponse: Файл главной страницы
    """
    return FileResponse(BASE_DIR/"static/index.html")


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
