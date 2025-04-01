from fastapi import APIRouter
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation

from schemas.auth import UserCreate, Token
from models.users import User
from utils.security import create_access_token, hash_password
from utils.database import get_session
from utils.exceptions import raise_user_exists_exception, raise_bad_request_exception, raise_internal_error_exception

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token)
async def create_user(user: UserCreate):
    user_id = None

    if user.password != user.confirm_password:
        raise_bad_request_exception("Passwords do not match")
    
    with get_session() as session:
        try:
            result = session.execute(
                sa.insert(User).values(
                    email=user.email,
                    password=hash_password(user.password)
                ).returning(User.id)
            )
            session.commit()
            user_id = result.scalar_one()
        except IntegrityError as e:
            session.rollback()
            orig = getattr(e, 'orig', None)

            if isinstance(orig, UniqueViolation):
                pg_code = getattr(orig, 'sqlstate', None)
                if pg_code == '23505':
                    raise_user_exists_exception(f"User with email '{user.email}' already exists")

            raise_bad_request_exception(f"Database constraint violated: {str(e)}")

    # QUESTION: Should I validate it or not?
    if user_id is None:
        raise_internal_error_exception("Failed to create user")

    access_token = create_access_token(
        data={"email": user.email, "uid": user_id}
    )

    return {"access_token": access_token, "token_type": "bearer"}
