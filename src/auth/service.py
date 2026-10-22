"""Модуль бизнес-логики для сервиса Регистрации/Авторизации"""
from datetime import UTC, datetime

from sqlalchemy import exists, select

from src.config import settings
from src.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

from .models import UserData, UserTokenData

SECONDS_IN_MINUTE = 60
SECONDS_IN_DAY = 86400


def create_new_user(username: str, email: str, password: str, db) -> dict:
    """Создание нового пользователя

    Args:
        username (str): Имя юзера
        email (str): Почта юзера
        password (str): Пароль юзера
        db (_type_): Объект сессии БД

    Returns:
        dict: Словарь с данными для coockie
    """
    if (db.scalar(select(exists().where(UserData.email == email)))):
        pass
    else:
        hashed_password = hash_password(password)
        user_object = UserData(
            username=username,
            email=email,
            hash_password=hashed_password
        )
        db.add(user_object)
        db.commit()
        access_token = create_access_token({"sub": str(user_object.id)})
        refresh_token = create_refresh_token({"sub": str(user_object.id)})
        join_user_token(refresh_token, db)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES*SECONDS_IN_MINUTE,
            "refresh_expires_in": settings.REFRESH_TOKEN_EXPIRE_DAYS*SECONDS_IN_DAY,
            "token_type": "bearer"
        }


def authenticate_user(email: str, password: str, db) -> dict:
    """Авторизация старого пользователя

    Args:
        username (str): Имя юзера
        email (str): Почта юзера
        password (str): Пароль юзера
        db (_type_): Объект сессии БД

    Returns:
        dict: Словарь с данными для coockie
    """
    if (db.scalar(select(exists().where(UserData.email == email)))):
        user_object = db.scalars(
            select(UserData).where(UserData.email == email)
        ).one()
        if verify_password(password, user_object.password):
            access_token = create_access_token({"sub": str(user_object.id)})
            refresh_token = create_refresh_token({"sub": str(user_object.id)})
            join_user_token(refresh_token, db)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES*SECONDS_IN_MINUTE,
                "refresh_expires_in": settings.REFRESH_TOKEN_EXPIRE_DAYS*SECONDS_IN_DAY,
                "token_type": "bearer"
            }
        else:
            pass
    else:
        pass


def join_user_token(refresh_token: str, db):
    """Привязка токена к пользователю

    Args:
        refresh_token (str): refresh токен
        db (_type_): Объект сессии БД
    """
    data = decode_token(refresh_token)
    if db.scalar(select(exists().where(UserTokenData.user_id == data["sub"]))):
        usertoken_object = db.scalars(
            select(UserTokenData).where(UserTokenData.id == data["sub"])
        ).one()
        usertoken_object.token = refresh_token
        usertoken_object.created_at = datetime.now(UTC)
        usertoken_object.expires_at = datetime.fromtimestamp(data["exp"])
    else:
        usertoken_object = UserTokenData(
            token=refresh_token,
            created_at=datetime.now(UTC),
            expired_at=datetime.fromtimestamp(data["exp"]),
            user_id=data["sub"])
        db.add(usertoken_object)
    db.commit()
