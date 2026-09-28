from pathlib import Path

import uvicorn
from fastapi import Cookie, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from auth import auth_router

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR/"static"))
app.include_router(auth_router)


@app.get("/")
def index(refresh_token: str = Cookie(None)):
    """Точка входа"""
    return FileResponse(BASE_DIR/"static/index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
