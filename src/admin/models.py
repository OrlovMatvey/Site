"""Модуль ORM-моделей БД для сервиса Администрации"""
from datetime import UTC, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class AdminLog(Base):
    """Модель для таблицы с админ-логами"""
    __tablename__ = "AdminLog"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int] = mapped_column(
        ForeignKey(column="UserData.id", ondelete="SET NULL")
    )
    action: Mapped[str] = mapped_column(String(20))
    table_name: Mapped[str] = mapped_column(String(50))
    record_id: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC)
    )
    # Реализовать логи
