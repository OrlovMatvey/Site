from pydantic import BaseModel


class AuthenticateModel(BaseModel):
    username: str
    email: str
    password: str
