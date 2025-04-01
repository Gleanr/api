from fastapi import APIRouter, HTTPException, status
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation

from schemas.auth import UserBase, Token
from models.users import User
from utils.security import create_access_token
from utils.database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


def fake_hash_password(password: str):
    return "fakehashed_" + password


@router.post("/signup", response_model=Token)
async def create_user(user: UserBase):
    user_id = None
    
    with get_session() as session:
        try:
            result = session.execute(
                sa.insert(User).values(
                    email=user.email,
                    password=fake_hash_password(user.password)
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
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"User with email '{user.email}' already exists"
                    )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database constraint violated: {str(e)}"
            )

    # QUESTION: Should I validate it or not?
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    access_token = create_access_token(
        data={"email": user.email, "uid": user_id}
    )

    return {"access_token": access_token, "token_type": "bearer"}
