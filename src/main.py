"""Главный модуль запуска приложения"""
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from auth import auth_router

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR/"static"))
app.include_router(auth_router)


@app.get("/")
def index() -> FileResponse:
<<<<<<< HEAD
    """Точка входа

    Returns:
        FileResponse: Файл главной страницы
    """
=======
    """Вход в приложение"""
>>>>>>> cbea4c1a8eee79ca0c991f04ab38dc5d4248b6f5
    return FileResponse(BASE_DIR/"static/index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
