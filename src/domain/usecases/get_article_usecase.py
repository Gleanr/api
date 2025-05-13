from domain.daos.article_db import ArticleDbDAO
from utils.exceptions import raise_bad_request_exception, raise_internal_error_exception


class GetArticleUsecase:
    def __init__(self, article_db_dao: ArticleDbDAO):
        self.article_db_dao = article_db_dao

    def execute(self, user_id: str, article_id: str):
        try:
            return self.article_db_dao.get_details(user_id, article_id)

        except ArticleDbDAO.ArticleNotFoundError:
            raise_bad_request_exception("Article not found or not accessible")
        except Exception as e:
            raise_internal_error_exception(str(e))