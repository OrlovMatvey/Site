"""Модуль за зависимостей FastAPI"""
from collections.abc import Iterator

from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy import exists, select
from sqlalchemy.orm import Session, sessionmaker

from src.auth import UserTokenData
from src.database import engine
from src.security import create_access_token, decode_token

session = sessionmaker(engine)


def get_db() -> Iterator[Session]:
    """Создание сессии БД

    Yields:
        Iterator[Session]: Объект сессии БД
    """
    try:
        db = session()
        yield db
    finally:
        db.close()


def is_authenticated(request: Request, response: Response, db: Session = Depends(get_db)) -> bool:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token and decode_token(access_token):
        return True
    if refresh_token:
        data = decode_token(refresh_token)
        if data:
            user_id = data["sub"]
            db_token = db.scalar(select(exists().where(
                UserTokenData.user_id == user_id, UserTokenData.token == refresh_token
            )))
            if db_token:
                new_access_token = create_access_token({"sub": user_id})
                response.set_cookie(
                    key="access_token",
                    value=new_access_token["access_token"],
                    domain="127.0.0.1",
                    httponly=True,
                    max_age=new_access_token["access_expires_in"]
                )
                return True

    raise HTTPException(status_code=401, detail="Пользователь не авторизован")
