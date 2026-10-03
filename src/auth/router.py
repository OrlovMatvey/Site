from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse

from .service import create_user
from .schemas import AuthenticateModel

router = APIRouter(tags=['Authentication'])


@router.post("/auth")
def authenticate(request: AuthenticateModel, response: Response) -> RedirectResponse:
    create_user(request.model_dump())
    response.set_cookie()
    response.set_cookie()
    return RedirectResponse(url="/")
