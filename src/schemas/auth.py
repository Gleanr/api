from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
