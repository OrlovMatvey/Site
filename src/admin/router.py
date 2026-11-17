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
    is_deleted = delete_record_by_id(table_name, record_id, db)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Запись или таблица не найдена")
    return Response(status_code=203)


@router.post("/{table_name}/{record_id}")
async def update_record(
    table_name: str,
    record_id: int,
    request: Request,
    db: Session = Depends(get_db)
) -> Response:
    record_data = await request.json()
    is_updated = update_record_by_id(table_name, record_id, record_data, db)
    if not is_updated:
        raise HTTPException(
            status_code=500, detail="Ошибка при обновлении записи"
        )
    Response(status_code=200)
