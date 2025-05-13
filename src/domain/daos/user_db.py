import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from models.user import User
from utils.security import hash_password
from utils.database import get_session


class UserDAO:
    class UserAlreadyExistsError(Exception):
        pass

    class UserNotFoundError(Exception):
        pass

    def get_by_email(self, email: str):
        with get_session() as session:
            try:
                result = session.execute(
                    sa.select(User).where(User.email == email)
                )
                user = result.scalar_one_or_none()
            except IntegrityError as e:
                raise e

        if not user:
            raise self.UserNotFoundError

        return user


    def insert_user(self, email: str, password: str):
        with get_session() as session:
            try:
                result = session.execute(
                    sa.insert(User).values(
                        email=email,
                        password=hash_password(password)
                    ).returning(User.id)
                )

                session.commit()
                return result.scalar_one()

            except IntegrityError as e:
                if "already exists" in e.orig.args[0]:
                    raise self.UserAlreadyExistsError
                raise e
