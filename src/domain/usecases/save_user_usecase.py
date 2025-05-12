from sqlalchemy.exc import IntegrityError
from domain.daos.user import UserDAO
from utils.security import create_access_token, verify_password
from utils.exceptions import raise_internal_error_exception, raise_user_exists_exception


class SaveUserUsecase:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def execute(self, email: str, password: str):
        try:
            user_id = self.user_dao.insert_user(user_email=email, user_password=password)
            access_token = create_access_token(
                data={"email": email, "uid": user_id}
            )

            return access_token

        except UserDAO.UserAlreadyExistsError:
            raise_user_exists_exception(f"User with email '{email}' already exists")

        except IntegrityError as e:
            raise_internal_error_exception(f"Database constraint violated: {str(e)}")
