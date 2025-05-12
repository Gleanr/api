from fastapi import APIRouter, Form
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from schemas.auth import User as UserLogin, UserCreate, Token
from models.user import User
from domain.daos.user import UserDAO
from domain.usecases.save_user_usecase import SaveUserUsecase
from utils.security import create_access_token, verify_password
from utils.database import get_session
from utils.exceptions import (
    raise_unauthorized_exception,
    raise_bad_request_exception,
    raise_internal_error_exception
)

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
async def login(data: UserLogin):
    user = None

    with get_session() as session:
        try:
            result = session.execute(
                sa.select(User).where(User.email == data.email)
            )
            user = result.scalar_one_or_none()
        except IntegrityError as e:
            session.rollback()
            raise_internal_error_exception(f"Database constraint violated: {str(e)}")

    if user is None:
        raise_unauthorized_exception("Invalid email or password")

    if not verify_password(data.password, user.password):
        raise_unauthorized_exception("Invalid email or password")

    access_token = create_access_token(
        data={"email": user.email, "uid": user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}


# This endpoint for OAuth2 form-based authentication DOCS login
@router.post("/token", response_model=Token)
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...)
):
    user = None

    with get_session() as session:
        try:
            result = session.execute(
                sa.select(User).where(User.email == username)
            )
            user = result.scalar_one_or_none()
        except IntegrityError as e:
            session.rollback()
            raise_internal_error_exception(f"Database constraint violated: {str(e)}")

    if user is None:
        raise_unauthorized_exception("Invalid email or password")

    if not verify_password(password, user.password):
        raise_unauthorized_exception("Invalid email or password")

    access_token = create_access_token(
        data={"email": user.email, "uid": user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=Token)
async def create_user(user: UserCreate):
    if user.password != user.confirm_password:
        raise_bad_request_exception("Passwords do not match")

    user_dao = UserDAO()
    usecase = SaveUserUsecase(user_dao)
    access_token = usecase.execute(email=user.email, password=user.password)

    return {"access_token": access_token, "token_type": "bearer"}
