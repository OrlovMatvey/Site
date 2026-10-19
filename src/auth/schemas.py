"""Модуль Pydantic схем для сервиса Регистрации/Авторизации"""
from fastapi import Form
from pydantic import BaseModel


class AuthenticateModel(BaseModel):
    username: str
    email: str
    password: str

    @classmethod
    def formBody(cls, username: Form(...), email: Form(...), password: Form(...)) -> AuthenticateModel:
        return cls(username, email, password)
