from domain.daos.article_db import ArticleDbDAO
from utils.exceptions import raise_internal_error_exception


class GetArticlesListUsecase:
    def __init__(self, article_db_dao: ArticleDbDAO):
        self.article_db_dao = article_db_dao

    def execute(self, user_id: str):
        try:
            return self.article_db_dao.get_list(user_id)

        except Exception as e:
            raise_internal_error_exception(str(e))