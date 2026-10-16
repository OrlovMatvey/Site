"""Модуль ORM-моделей БД для сервиса Регистрации/Авторизации"""
from datetime import date

from sqlalchemy import JSON, ForeignKey, LargeBinary, String
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


class ReceptData(Base):
    """Модель для таблицы с рецептами"""
    __tablename__ = "ReceptData"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    image: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[dict] = mapped_column(JSON, default=dict)
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
    category: Mapped[int] = mapped_column(ForeignKey('CategoryData.id'))
    count_likes: Mapped[int] = mapped_column()
    count_dislikes: Mapped[int] = mapped_column()


class CommentData(Base):
    """Модель для таблицы с комментариями"""
    __tablename__ = "CommentData"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(1000))
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
    recept_id: Mapped[int] = mapped_column(ForeignKey('ReceptData.id'))


class FavoriteReceptData(Base):
    """Модель для таблицы с избранными рецептами"""
    __tablename__ = "FavoriteReceptData"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('UserData.id'))
    recept_id: Mapped[int] = mapped_column(ForeignKey('ReceptData.id'))


class IngredientData(Base):
    """Модель для таблицы с ингредиентами"""

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(50))


class CategoryData(Base):
    """Модель для таблицы с категориями"""

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(50))
