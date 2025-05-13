from fastapi import APIRouter, Form

from schemas.auth import User as UserLogin, UserCreate, Token
from domain.daos.user_db import UserDAO
from domain.usecases.save_user_usecase import SaveUserUsecase
from domain.usecases.get_user_usecase import GetUserUsecase
from utils.exceptions import raise_bad_request_exception

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    user_dao = UserDAO()
    usecase = GetUserUsecase(user_dao)
    access_token = usecase.execute(email=user.email, password=user.password)

    return {"access_token": access_token, "token_type": "bearer"}


# This endpoint for OAuth2 form-based authentication DOCS login
@router.post("/token", response_model=Token)
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...)
):
    user_dao = UserDAO()
    usecase = GetUserUsecase(user_dao)
    access_token = usecase.execute(email=username, password=password)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=Token)
async def create_user(user: UserCreate):
    if user.password != user.confirm_password:
        raise_bad_request_exception("Passwords do not match")

    user_dao = UserDAO()
    usecase = SaveUserUsecase(user_dao)
    access_token = usecase.execute(email=user.email, password=user.password)

    return {"access_token": access_token, "token_type": "bearer"}
