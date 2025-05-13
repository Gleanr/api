from sqlalchemy.exc import IntegrityError
from domain.daos.user_db import UserDAO
from utils.security import create_access_token, verify_password
from utils.exceptions import raise_internal_error_exception, raise_unauthorized_exception


class GetUserUsecase:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def execute(self, email: str, password: str):
        try:
            user = self.user_dao.get_by_email(email=email)

            if not verify_password(plain_password=password, hashed_password=user.password):
                raise_unauthorized_exception("Invalid email or password")

            access_token = create_access_token(
                data={"email": user.email, "uid": user.id}
            )

            return access_token

        except UserDAO.UserNotFoundError:
            raise_unauthorized_exception("Invalid email or password")

        except IntegrityError as e:
            raise_internal_error_exception(f"Database constraint violated: {str(e)}")
