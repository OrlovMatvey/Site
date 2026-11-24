"""Модуль эндпоинтов для сервиса Администрации"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from src.common import TEMPLATES
from src.dependencies import get_current_admin, get_db

from .service import delete_record_by_id, get_table_data_from_db, update_record_by_id

router = APIRouter(
    prefix="/Admin", tags=["AdminProcess"],
    dependencies=[Depends(get_current_admin)]
)


@router.get("/")
def get_admin_page(
    request: Request,
    table: str = "User",
    db: Session = Depends(get_db)
) -> HTMLResponse:
    """Эндпоинт для получения страницы админ-панели

    Args:
        request (Request): Тело запроса.
        table (str, optional): Имя текущей таблицы.
        db (Session, optional): Объект сессии в БД.

    Returns:
        HTMLResponse: Возращает шаблон страницы админ-панели
    """
    panel_data = get_table_data_from_db(table, db)
    return TEMPLATES.TemplateResponse(
        request=request, name="admin.html", context={
            "fields": panel_data["fields"],
            "records": panel_data["records"],
            "active_table": table
        }
    )


@router.delete("/{table_name}/{record_id}")
def delete_record(
    table_name: str,
    record_id: int,
    db: Session = Depends(get_db)
) -> Response:
    """Эндпоинт для удаления конкретной записи из БД

    Args:
        table_name (str): Имя текущей таблицы.
        record_id (int): ID выбранной записи.
        db (Session, optional): Объект сессии в БД.

    Raises:
        HTTPException: Запись или таблица не найдена.

    Returns:
        Response: Пустой ответ, код 204.
    """
    delete_record_by_id(table_name, record_id, db)
    return Response(status_code=204)


@router.post("/{table_name}/{record_id}")
async def update_record(
    table_name: str,
    record_id: int,
    request: Request,
    db: Session = Depends(get_db)
) -> Response:
    """Эндпоинт для обновления конкретной записи из БД

    Args:
        table_name (str): Имя текущей таблицы.
        record_id (int): ID выбранной записи.
        request (Request): Тело запроса.
        db (Session, optional): Объект сессии в БД.

    Raises:
        HTTPException: Ошибка при обновлении записи

    Returns:
        Response: Пустой ответ, код 204.
    """
    record_data = await request.json()
    update_record_by_id(table_name, record_id, record_data, db)
    return Response(status_code=204)
