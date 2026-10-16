"""Модуль бизнес-логики для сервиса Регистрации/Авторизации"""
from sqlalchemy import select

from src.dependencies import get_db
from src.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

from .models import UserData


def new_user(username: str, email: str, password: str, db) -> dict:
    """Создание нового пользователя

    Args:
        username (str): Имя юзера
        email (str): Почта юзера
        password (str): Пароль юзера
        db (_type_): Объект сессии БД

    Returns:
        dict: Словарь с данными для coockie
    """
    hashed_password = hash_password(password)
    user_object = UserData(username, email, hashed_password)
    db.add(user_object)
    db.commit()
    access_token = create_access_token({"sub": user_object.id})
    refresh_token = create_refresh_token({"sub": user_object.id})
    join_user_token(refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 3600,
        "token_type": "bearer"
    }


def auth_user(username: str, email: str, password: str, db) -> dict:
    """Авторизация старого пользователя

    Args:
        username (str): Имя юзера
        email (str): Почта юзера
        password (str): Пароль юзера
        db (_type_): Объект сессии БД

    Returns:
        dict: Словарь с данными для coockie
    """
    user_object = db.scalars(select(UserData).where(UserData.email == email)).one()
    if verify_password(password, user_object.password):
        access_token = create_access_token({"sub": user_object.id})
        refresh_token = create_refresh_token({"sub": user_object.id})
        join_user_token(refresh_token)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 3600,
            "token_type": "bearer"
        }


def join_user_token():
    pass


auth_user("Deceptor", "deceptor27@mail.ru", "password", db=next(get_db()))
