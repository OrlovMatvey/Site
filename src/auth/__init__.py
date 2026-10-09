"""Модуль инициализации пакета для сервиса Регистрации/Авторизации"""
from .models import Base, UserData, UserTokens
from .router import router as auth_router

__all__ = [
    "UserData",
    "UserTokens",
    "auth_router",
]
