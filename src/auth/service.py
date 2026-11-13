"""Модуль бизнес-логики для сервиса Регистрации/Авторизации"""
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import settings
from src.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

from .models import UserData, UserTokenData


def create_new_user(username: str, email: str, password: str, db: Session) -> dict[str, str | int]:
    """Создание нового пользователя

    Args:
        username (str): Имя юзера.
        email (str): Почта юзера.
        password (str): Пароль юзера.
        db (_type_): Объект сессии БД.

    Returns:
        dict[str, str | int]: Словарь с данными для coockie.
    """
    if db.scalar(select(UserData).where(UserData.email == email)):
        raise HTTPException(status_code=409, detail="Данный email уже занят.")
    else:
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
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_expires_in": timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "refresh_expires_in": timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "token_type": "bearer"
        }


def authenticate_user(email: str, password: str, db: Session) -> dict[str, str | int]:
    """Авторизация старого пользователя

    Args:
        username (str): Имя юзера.
        email (str): Почта юзера.
        password (str): Пароль юзера.
        db (_type_): Объект сессии БД.

    Returns:
        dict[str, str | int]: Словарь с данными для coockie.
    """
    if db.scalar(select(UserData).where(UserData.email == email)):
        user_object = db.scalars(
            select(UserData).where(UserData.email == email)
        ).one()
        if verify_password(password, user_object.hash_password):
            access_token = create_access_token({"sub": str(user_object.id)})
            refresh_token = create_refresh_token({"sub": str(user_object.id)})
            join_user_token(refresh_token, db)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_expires_in": timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                "refresh_expires_in": timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
                "token_type": "bearer"
            }
        else:
            raise HTTPException(status_code=400, detail="Неверный логин или пароль.")
    else:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль.")


def join_user_token(user_id: int, refresh_token: str, db: Session) -> None:
    """Привязка токена к пользователю

    Args:
        refresh_token (str): refresh токен.
        db (_type_): Объект сессии БД.
    """
    now = datetime.now(UTC)
    exp = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    if db.scalar(select(UserTokenData).where(UserTokenData.user_id == user_id)):
        usertoken_object = db.scalar(
            select(UserTokenData).where(UserTokenData.user_id == user_id)
        )
        usertoken_object.token = refresh_token
        usertoken_object.created_at = datetime.now(UTC)
        usertoken_object.expires_at = datetime.fromtimestamp(exp)
    else:
        usertoken_object = UserTokenData(
            token=refresh_token,
            created_at=datetime.now(UTC),
            expired_at=datetime.fromtimestamp(exp),
            user_id=user_id)
        db.add(usertoken_object)
    db.commit()


def delete_refresh_token(refresh_token: str, db: Session) -> None:
    """Удаление refresh токена пользователя

    Args:
        refresh_token (str): Refresh token.
        db (Session): Объект сессии БД.
    """
    usertoken_object = db.scalar(select(UserTokenData).where(UserTokenData.token == refresh_token))
    if usertoken_object:
        db.delete(usertoken_object)
        db.commit()
