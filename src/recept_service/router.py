from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from src.config import settings
from src.dependencies import is_authenticated

router = APIRouter(prefix="/Service", tags=["BusinessProcess"])


@router.get("/Main")
def index_page(request: Request, authenticated: bool = Depends(is_authenticated)) -> HTMLResponse:
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="index.html"
    )


@router.get("/Profile")
def profile_page(request: Request, authenticated: bool = Depends(is_authenticated)) -> HTMLResponse:
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="profile.html"
    )


@router.get("/Admin")
def admin_pagedef(request: Request, authenticated: bool = Depends(is_authenticated)) -> HTMLResponse:
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="admin.html"
    )
