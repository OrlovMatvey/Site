"""Модуль эндпоинтов для сервиса Регистрации/Авторизации"""
from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from dependencies import get_db

from .schemas import AuthenticateModel
from .service import auth_user, new_user

router = APIRouter(prefix="Auth", tags=['AccessControl'])


@router.post("/UserUp")
def up_user(request: AuthenticateModel, response: Response, db: Session = Depends(get_db)) -> RedirectResponse:
    new_user(request.model_dump())
    response.set_cookie()
    response.set_cookie()
    return RedirectResponse(url="/")


@router.post("/UserIn")
def in_user(request: AuthenticateModel, response: Response, db: Session = Depends(get_db)) -> RedirectResponse:
    auth_user(request.model_dump())
    response.set_cookie()
    response.set_cookie()
    return RedirectResponse(url="/")
