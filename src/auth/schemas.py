"""Модуль Pydantic схем для сервиса Регистрации/Авторизации"""
from typing import Self

from fastapi import Form
from pydantic import BaseModel, EmailStr


class RegisterModel(BaseModel):
    """Pydantic-модель для валидации запроса на регистрацию

    Args:
        BaseModel (_type_): Базовый класс для Pydantic-моделей.

    Returns:
        _type_: Экземпляр модели.
    """
    username: str
    email: EmailStr
    password: str

    @classmethod
    def formBody(
        cls,
        username: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...)
    ) -> Self:
        return cls(username=username, email=email, password=password)


class LoginModel(BaseModel):
    """Pydantic-модель для валидации запроса на авторизацию

    Args:
        BaseModel (_type_): Базовый класс для Pydantic-моделей.

    Returns:
        _type_: Экземпляр модели.
    """
    email: EmailStr
    password: str

    @classmethod
    def formBody(
        cls,
        email: EmailStr = Form(...),
        password: str = Form(...)
    ) -> Self:
        return cls(email=email, password=password)


class TokenCookiesModel(BaseModel):
    """Pydantic-модель для cookie токенов

    Args:
        BaseModel (_type_): Базовый класс для Pydantic-моделей.
    """
    access_token: str
    refresh_token: str
    access_expires_in: int
    refresh_expires_in: int
