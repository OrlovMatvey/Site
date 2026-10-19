"""Модуль эндпоинтов для сервиса Регистрации/Авторизации"""
from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db

from .schemas import AuthenticateModel
from .service import auth_user, new_user

router = APIRouter(prefix="/Auth", tags=['AccessControl'])


@router.post("/UserUp")
def up_user(request: AuthenticateModel = Depends(AuthenticateModel.formBody()), response: Response, db: Session = Depends(get_db)) -> RedirectResponse:
    coockie_data = new_user(request.username, request.email, request.password, db)
    response.set_cookie(key="access_token", value=coockie_data["access_token"], max_age=coockie_data["access_expires_in"])
    response.set_cookie(key="refresh_token", value=coockie_data["refresh_token"], max_age=coockie_data["refresh_expires_in"])
    return RedirectResponse(url="/")


@router.post("/UserIn")
def in_user(request: AuthenticateModel, response: Response, db: Session = Depends(get_db)) -> RedirectResponse:
    coockie_data = auth_user(request.email, request.password, db)
    response.set_cookie(key="access_token", value=coockie_data["access_token"], max_age=coockie_data["access_expires_in"])
    response.set_cookie(key="refresh_token", value=coockie_data["refresh_token"], max_age=coockie_data["refresh_expires_in"])
    return RedirectResponse(url="/")
