"""Модуль Pydantic схем для сервиса Регистрации/Авторизации"""
from typing import Self

from fastapi import Form
from pydantic import BaseModel


class RegisterModel(BaseModel):
    """Pydantic-модель для валидации запроса на регистрацию

    Args:
        BaseModel (_type_): Базовый класс для моделей

    Returns:
        _type_: Экземпляр модели
    """
    username: str
    email: str
    password: str

    @classmethod
    def formBody(cls, username: str = Form(...), email: str = Form(...), password: str = Form(...)) -> Self:
        return cls(username=username, email=email, password=password)


class LoginModel(BaseModel):
    """Pydantic-модель для валидации запроса на авторизацию

    Args:
        BaseModel (_type_): Базовый класс для моделей

    Returns:
        _type_: Экземпляр модели
    """
    email: str
    password: str

    @classmethod
    def formBody(cls, email: str = Form(...), password: str = Form(...)) -> Self:
        return cls(email=email, password=password)
