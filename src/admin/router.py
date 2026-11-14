"""Модуль эндпоинтов для сервиса Администрации"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.common import TEMPLATES
from src.dependencies import get_current_admin, get_db

from .service import delete_row_by_id, get_admin_dashboard_data, update_row_by_id

router = APIRouter(
    prefix="/Admin", tags=["AdminProcess"],
    dependencies=[Depends(get_current_admin)]
)


@router.get("/")
def get_admin_page(
    request: Request,
    table: str = "users",
    db: Session = Depends(get_db)
) -> HTMLResponse:
    panel_data = get_admin_dashboard_data(db, table_name=table)
    return TEMPLATES.TemplateResponse(
        request=request, name="admin.html", context={
            "request": request,
            "fields": panel_data["fields"],
            "rows": panel_data["rows"],
            "title_table": panel_data["verbose_name"],
            "active_table": table
        }
    )


@router.delete("/{table}/{id}", status_code=200)
def delete_table_row(table: str, id: int, db: Session = Depends(get_db)):
    """Универсальное удаление записи из любой таблицы"""
    success = delete_row_by_id(db, table_name=table, row_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return {"status": "success", "message": "Запись успешно удалена"}


@router.post("/{table}/{id}", status_code=200)
async def update_table_row(table: str, id: int, request: Request, db: Session = Depends(get_db)):
    """Универсальное обновление записи"""
    # Получаем данные, которые админ отправил из формы модального окна
    form_data = await request.json() 
    success = update_row_by_id(db, table_name=table, row_id=id, data=form_data)
    if not success:
        raise HTTPException(status_code=400, detail="Не удалось изменить")
    return {"status": "success", "message": "Запись успешно обновлена"}
