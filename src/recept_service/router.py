from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.config import settings

router = APIRouter(prefix="/Service", tags=["BusinessProcess"])


@router.get("/Main")
def index_page(request: Request) -> HTMLResponse:
    return settings.TEMPLATES.TemplateResponse(request=request, name="index.html")


@router.get("/Profile")
def profile_page(request: Request) -> HTMLResponse:
    return settings.TEMPLATES.TemplateResponse(request=request, name="profile.html")
