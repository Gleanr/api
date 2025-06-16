from sqlalchemy.exc import IntegrityError
from domain.daos.article_web import ArticleWebDAO
from domain.daos.article_db import ArticleDbDAO
from utils.exceptions import raise_internal_error_exception


class SaveArticleUsecase:
    def __init__(self, article_db_dao: ArticleDbDAO, article_web_dao: ArticleWebDAO):
        self.article_db_dao = article_db_dao
        self.article_web_dao = article_web_dao

    def execute(self, url: str, user_id: str):
        try:
            existing_article = self.article_db_dao.get_by_url(url)
            self.article_db_dao.insert_user_article(user_id, article_id=existing_article['id'])

            return existing_article

        except ArticleDbDAO.UserArticleAlreadyExistsError:
            return existing_article

        except ArticleDbDAO.ArticleNotFoundError:
            new_article = self.article_web_dao.get(url)

            new_article_data = self.article_db_dao.insert_article(new_article)
            self.article_db_dao.insert_user_article(user_id, new_article_data['id'])

            return new_article_data

        except IntegrityError as e:
            raise_internal_error_exception(f"Database constraint violated: {str(e)}")

