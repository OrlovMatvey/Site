"""Модуль эндпоинтов для Администрации"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from src.config import settings
from src.dependencies import get_current_admin

router = APIRouter(prefix="/Admin", tags=["AdminProcess"])


@router.get("/")
def get_admin_page(
    request: Request,
    admin: bool = Depends(get_current_admin)
) -> HTMLResponse:
    context = {"is_admin": admin}
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="admin.html", context=context
    )
