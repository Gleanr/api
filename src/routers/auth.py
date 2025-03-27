from fastapi import APIRouter, Depends

from schemas.auth import UserBase, Token
from utils.exceptions import user_exists_exception, raise_unauthorized_exception
from utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

fake_users_db = {}


def fake_hash_password(password: str):
    return "fakehashed_" + password


@router.post("/signup", response_model=Token)
async def create_user(user: UserBase):
    if not user.email or not user.password:
        raise_unauthorized_exception("Email and password are required.")

    if user.email in fake_users_db:
        user_exists_exception()

    fake_users_db[user.email] = {
        "email": user.email,
        "hashed_password": fake_hash_password(user.password)
    }

    access_token = create_access_token(
        data={"email": user.email, "uid": "123"}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
