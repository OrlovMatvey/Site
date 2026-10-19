"""Модуль Pydantic схем для сервиса Регистрации/Авторизации"""
from typing import Self

from fastapi import Form
from pydantic import BaseModel


class AuthenticateModel(BaseModel):
    username: str
    email: str
    password: str

    @classmethod
    def formBody(cls, username: str = Form(...), email: str = Form(...), password: str = Form(...)) -> Self:
        return cls(username=username, email=email, password=password)
