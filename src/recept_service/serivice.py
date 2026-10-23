from sqlalchemy.orm import Session
from sqlalchemy import select
from src.security import decode_token
from src.auth import UserData
from .models import ReceptData


def get_records_from_db(access_token: str, db: Session):
    user_data: dict
    recepts_data: list
    token_data = decode_token(access_token)
    user_data = db.scalar(select(UserData).where(UserData.id == token_data["sub"]))
    user_data = user_data.get_dict()
    recepts = db.scalars(select(ReceptData).where(ReceptData.user_id == token_data["sub"]))
    for recept in recepts:
        recepts_data.append(recept.get_dict())