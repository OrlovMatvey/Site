"""Модуль бизнес-логики для сервиса Регистрации/Авторизации"""
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import settings
from src.exceptions import ConflictError, IncorrectInput, NotFoundError
from src.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

from .models import UserData, UserTokenData
from .schemas import TokenCookiesModel


def create_new_user(
    username: str,
    email: str,
    password: str,
    db: Session
) -> TokenCookiesModel:
    """Создание нового пользователя

    Args:
        username (str): Имя пользователя.
        email (str): Почта пользователя.
        password (str): Пароль пользователя.
        db (_type_): Объект сессии БД.

    Raises:
        ConflictError: Данный email уже занят.

    Returns:
        TokenCookiesModel: Объект с данными для coockie.
    """
    if db.scalar(select(UserData).where(UserData.email == email)):
        raise ConflictError()
    
    hashed_password = hash_password(password)
    user_object = UserData(
        username=username,
        email=email,
        hash_password=hashed_password
    )
    db.add(user_object)
    db.flush()
    access_token = create_access_token({"sub": str(user_object.id)})
    refresh_token = create_refresh_token({"sub": str(user_object.id)})
    join_user_token(user_object.id, refresh_token, db)
    return TokenCookiesModel(
        access_token=access_token,
        refresh_token=refresh_token,
        access_expires_in=int(timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ).total_seconds()),
        refresh_expires_in=int(timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ).total_seconds())
    )


def authenticate_user(
    email: str,
    password: str,
    db: Session
) -> TokenCookiesModel:
    """Авторизация старого пользователя

    Args:
        email (str): Почта пользователя.
        password (str): Пароль пользователя.
        db (_type_): Объект сессии БД.

    Raises:
        IncorrectLoginInput: Неверный логин или пароль.

    Returns:
        TokenCookiesModel: Объект с данными для cookie.
    """
    user_object = db.scalar(select(UserData).where(UserData.email == email))
    if not user_object or not verify_password(password, user_object.hash_password):
        raise IncorrectInput(detail="Неверный логин или пароль")
    
    access_token = create_access_token({"sub": str(user_object.id)})
    refresh_token = create_refresh_token({"sub": str(user_object.id)})
    join_user_token(user_object.id, refresh_token, db)
    return TokenCookiesModel(
        access_token=access_token,
        refresh_token=refresh_token,
        access_expires_in=int(timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ).total_seconds()),
        refresh_expires_in=int(timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ).total_seconds())
    )


def join_user_token(user_id: int, refresh_token: str, db: Session) -> None:
    """Привязка токена к пользователю

    Args:
        user_id (int): ID текущего пользователя.
        refresh_token (str): Refresh token.
        db (_type_): Объект сессии БД.
    """
    now = datetime.now(UTC)
    exp = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    usertoken_object = db.scalar(
        select(UserTokenData).where(UserTokenData.user_id == user_id)
    )
    if usertoken_object:
        usertoken_object.token = refresh_token
        usertoken_object.created_at = now
        usertoken_object.expires_at = exp
    else:
        usertoken_object = UserTokenData(
            token=refresh_token,
            created_at=now,
            expired_at=exp,
            user_id=user_id)
        db.add(usertoken_object)
    db.commit()


def delete_refresh_token(refresh_token: str, db: Session) -> None:
    """Удаление refresh токена пользователя

    Args:
        refresh_token (str): Refresh token.
        db (Session): Объект сессии БД.
    Raises:
        NotFoundError: Refresh токен не найден.
    """
    usertoken_object = db.scalar(
        select(UserTokenData).where(UserTokenData.token == refresh_token)
    )
    if not usertoken_object:
        raise NotFoundError(detail="Refresh токен не найден")
    db.delete(usertoken_object)
    db.commit()
    
