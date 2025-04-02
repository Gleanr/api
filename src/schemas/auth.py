from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str


class UserCreate(User):
    confirm_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
