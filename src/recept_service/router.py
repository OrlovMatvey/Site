from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.config import settings
from src.dependencies import is_authenticated, get_db

from .schemas import RecipeModel
from .serivice import get_profile_from_db, add_new_recipe

router = APIRouter(prefix="/Service", tags=["BusinessProcess"])


@router.get("/Main")
def get_index_page(
    request: Request, 
    authenticated: bool = Depends(is_authenticated)
) -> HTMLResponse:
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="index.html"
    )


@router.get("/Profile")
def get_profile_page(
    request: Request, 
    authenticated: bool = Depends(is_authenticated), 
    db: Session = Depends(get_db)
) -> HTMLResponse:
    access_token = request.cookies.get("access_token")
    if not access_token:
        access_token = authenticated
    context = get_profile_from_db(access_token, db)
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="profile.html", context=context
    )


@router.get("/Admin")
def get_admin_page(
    request: Request, 
    authenticated: bool = Depends(is_authenticated)
) -> HTMLResponse:
    return settings.TEMPLATES.TemplateResponse(
        request=request, name="admin.html"
    )


@router.post("/Profile")
def create_recipe(
    request: Request = Depends(RecipeModel.formBody),
    authenticated: bool = Depends(is_authenticated),
    db: Session = Depends(get_db)
):
    access_token = request.cookies.get("access_token")
    add_new_recipe(
        access_token,
        request.title, request.category,
        request.body, request.ingredient_name,
        request.ingredient_volume, request.ingredient_unit,
        request.image, db
        )
