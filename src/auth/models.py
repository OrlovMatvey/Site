"""Модуль ORM-моделей БД для сервиса Регистрации/Авторизации"""
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UserData(Base):
    """Модель для таблицы с данными пользователей"""
    __tablename__ = "UserData"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(40))
    hash_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)


class UserToken(Base):
    """Модель для таблицы с токенами пользователей"""
    __tablename__ = "UserTokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[date] = mapped_column()
    expired_at: Mapped[date] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
