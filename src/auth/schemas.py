from pydantic import BaseModel


class UserUpModel(BaseModel):
    username: str
    email: str
    password: str
