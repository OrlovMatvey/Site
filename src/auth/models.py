"""Модуль ORM-моделей БД для сервиса Регистрации/Авторизации"""
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для моделей"""
    @classmethod
    def fields(cls) -> list:
        """Вывод полей для модели

        Returns:
            list: Список полей модели
        """
        return [a.name for a in cls.__table__.columns]


class UserData(Base):
    """Модель для таблицы с данными пользователей"""
    __tablename__ = "UserData"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(40))
    hash_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)


class UserTokens(Base):
    """Модель для таблицы с токенами пользователей"""
    __tablename__ = "UserTokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[date] = mapped_column()
    expired_at: Mapped[date] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
