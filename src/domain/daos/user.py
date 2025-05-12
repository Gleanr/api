import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from models.user import User
from utils.security import hash_password
from utils.database import get_session


class UserDAO:
    class UserAlreadyExistsError(Exception):
        pass

    def insert_user(self, user_email: str, user_password: str):
        with get_session() as session:
            try:
                result = session.execute(
                    sa.insert(User).values(
                        email=user_email,
                        password=hash_password(user_password)
                    ).returning(User.id)
                )

                session.commit()
                return result.scalar_one()

            except IntegrityError as e:
                if "already exists" in e.orig.args[0]:
                    raise self.UserAlreadyExistsError
                raise e
