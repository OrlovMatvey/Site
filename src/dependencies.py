"""Модуль за зависимостей FastAPI"""
from collections.abc import Iterator

from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from src.auth import UserTokenData
from src.database import engine
from src.security import create_access_token, decode_token

session = sessionmaker(engine)


def get_db() -> Iterator[Session]:
    """Зависимость для создания сессии БД

    Yields:
        Iterator[Session]: Объект сессии БД
    """
    try:
        db = session()
        yield db
    finally:
        db.close()


def is_authenticated(request: Request, db: Session = Depends(get_db)) -> str:
    """Зависимость для проверки наличия токенов

    Args:
        request (Request): Тело запроса.
        db (Session, optional): Объект сессии БД. Defaults to Depends(get_db).

    Raises:
        HTTPException: Пользователь не авторизован

    Returns:
        str: Access_token(Новый или из cookie)
    """
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if access_token and decode_token(access_token):
        return access_token
    if refresh_token:
        data = decode_token(refresh_token)
        if data:
            user_id = data["sub"]
            db_token = db.scalars(select(UserTokenData).where(UserTokenData.user_id == data["sub"], UserTokenData.token == refresh_token)).one_or_none()
            if db_token:
                new_access_token = create_access_token({"sub": user_id})
                request.state.new_access_token = new_access_token
                return new_access_token

    raise HTTPException(status_code=401, detail="Пользователь не авторизован")
