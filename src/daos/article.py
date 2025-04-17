import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from models.article import Article
from models.associations import user_article
from utils.database import get_session


class ArticleDAO:
    class ArticleNotFoundError(Exception):
        pass

    class UserArticleAlreadyExistsError(Exception):
        pass

    def get_by_url(self, url: str) -> Article:
        with get_session() as session:
            result = session.execute(
                sa.select(Article).where(Article.url == url)
            )
            existing_article = result.scalar_one_or_none()

            if not existing_article:
                raise self.ArticleNotFoundError

            print(type(existing_article), existing_article)
            return existing_article

    def get_details(self, user_id: int, article_id: int) -> Article:
        with get_session() as session:
            result = session.execute(
                sa.select(Article)
                .join(user_article, Article.id == user_article.c.article_id)
                .where(
                    sa.and_(
                        Article.id == article_id,
                        user_article.c.user_id == user_id
                    )
                )
            )
            article = result.scalar_one_or_none()

            if not article:
                raise self.ArticleNotFoundError

            return article

    def get_list(self, user_id: int):
        with get_session() as session:
            result = session.execute(
                sa.select(
                    Article.id,
                    Article.title,
                    Article.description,
                    Article.site_name,
                    Article.created_at
                )
                .join(user_article, Article.id == user_article.c.article_id)
                .where(user_article.c.user_id == user_id)
                .order_by(Article.created_at.desc())
            )
            articles = [{
                "id": id,
                "title": title,
                "description": description,
                "site_name": site_name,
                "created_at": created_at
            }
                for id, title, description, site_name, created_at in result.all()]

            return articles

    def insert_user_article(self, user_id: int, article_id: int):
        with get_session() as session:
            session.execute(
                sa.insert(user_article).values(
                    user_id=user_id,
                    article_id=article_id
                )
            )

            try:
                session.commit()

            except IntegrityError as e:
                if "already exists" in e.orig.args[0]:
                    raise self.UserArticleAlreadyExistsError
                raise e

    def insert_article(self, article_data: dict[str, any]) -> int:
        with get_session() as session:
            result = session.execute(
                sa.insert(Article).values(**article_data).returning(Article.id)
            )
            article_id = result.scalar_one_or_none()

            try:
                session.commit()
                return article_id

            except IntegrityError as e:
                raise e
