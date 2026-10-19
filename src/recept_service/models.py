from sqlalchemy import JSON, ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


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
    __tablename__ = "IngredientData"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(50))


class CategoryData(Base):
    """Модель для таблицы с категориями"""
    __tablename__ = "CategoryData"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(50))
