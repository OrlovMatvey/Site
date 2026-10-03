"""Модуль для функций криптографии"""
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    """Хеширование пароля

    Args:
        password (str): Пароль с клиента

    Returns:
        str: Хеш пароля
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Проверка пароля на соответствие

    Args:
        password (str): Пароль с клиента
        hashed_password (str): Хеш пароля из БД

    Returns:
        bool: Результат сравнения(True/False)
    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    """Создание access jwt токена

    Args:
        data (dict): Информация для тела токена

    Returns:
        str: Кодированный токен
    """
    expire = datetime.timetz.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data["exp"] = expire
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def create_refresh_token(data: dict) -> str:
    """Создание refresh jwt токена

    Args:
        data (dict): Информация для тела токена

    Returns:
        str: Кодированный токен
    """
    expire = datetime.timetz.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    data["exp"] = expire
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    """Декодировка jwt токенов

    Args:
        token (str): Кодированный токен

    Returns:
        dict: Информация из тела токена
    """
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return data
