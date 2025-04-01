from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
