"""Модуль для функций криптографии"""
from passlib.context import CryptContext

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
        bool: Результат сравнения
    """
    return pwd_context.verify(password, hashed_password)

