"""Модуль за зависимостей FastAPI"""
from collections.abc import Iterator

from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from src.security import create_access_token, decode_token


def get_db() -> Iterator[Session]:
    """Зависимость для создания сессии БД

    Yields:
        Iterator[Session]: Объект сессии БД
    """
    from src.database import engine
    session = sessionmaker(engine)
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
    from src.auth import UserTokenData
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if access_token and decode_token(access_token):
        return access_token
    if refresh_token:
        data = decode_token(refresh_token)
        if data:
            user_id = data["sub"]
            db_token = db.scalar(select(UserTokenData).where(UserTokenData.user_id == data["sub"], UserTokenData.token == refresh_token))
            if db_token:
                new_access_token = create_access_token({"sub": user_id})
                request.state.new_access_token = new_access_token
                return new_access_token

    raise HTTPException(status_code=401, detail="Пользователь не авторизован")


def get_current_user(request: Request, access_token: str = Depends(is_authenticated), db: Session = Depends(get_db)) -> 'UserData':
    from src.auth import UserData
    user_id = decode_token(access_token)["sub"]
    user_object = db.scalar(select(UserData).where(UserData.id == user_id))

    request.state.user = user_object

    return user_object


def get_current_admin(user_object: 'UserData' = Depends(get_current_user)):
    if not user_object:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    
    if not user_object.is_admin:
        raise HTTPException(403, detail="Недостаточно прав доступа")
    return user_object.is_admin


def add_auth_context(request: Request):
    user = getattr(request.state, "user", None)
    return {
        "is_admin": getattr(user, "is_admin", False) if user else False
    }
