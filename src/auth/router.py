from fastapi import APIRouter
from schemas import UserUpModel

router = APIRouter(prefix="/auth", tags=['Authentication'])


@router.post("/up")
def user_up(user: UserUpModel):
    return True
