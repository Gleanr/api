from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import bcrypt
import jwt
from jwt.exceptions import PyJWTError
import sqlalchemy as sa

from config import get_settings
from models.users import User
from utils.database import get_session
from utils.exceptions import raise_credentials_exception_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

settings = get_settings()


def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise_credentials_exception_exception()
    except PyJWTError:
        raise_credentials_exception_exception()

    with get_session() as session:
        result = session.execute(
            sa.select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            raise_credentials_exception_exception()
            
        return user

