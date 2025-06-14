import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from domain.entities import ArticleEntity
from models.article import Article
from models.associations import user_article
from utils.database import get_session


class ArticleDbDAO:
    class ArticleNotFoundError(Exception):
        pass

    class UserArticleAlreadyExistsError(Exception):
        pass

    def get_by_url(self, url: str):
        with get_session() as session:
            result = session.execute(
                sa.select(
                    Article.id,
                    Article.title,
                    Article.description,
                    Article.site_name,
                    Article.created_at
                ).where(Article.url == url)
            )
            existing_article = result.first()

            if not existing_article:
                raise self.ArticleNotFoundError

            return {
                "id": existing_article.id,
                "title": existing_article.title,
                "description": existing_article.description,
                "site_name": existing_article.site_name,
                "created_at": existing_article.created_at
            }

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
            try:
                session.execute(
                    sa.insert(user_article).values(
                        user_id=user_id,
                        article_id=article_id
                    )
                )

                session.commit()

            except IntegrityError as e:
                if "already exists" in e.orig.args[0]:
                    raise self.UserArticleAlreadyExistsError
                raise e

    def insert_article(self, article_data: ArticleEntity) -> dict:
        with get_session() as session:
            result = session.execute(
                sa.insert(Article).values(**article_data.model_dump(exclude={"id", "created_at"})).returning(
                    Article.id,
                    Article.title,
                    Article.description,
                    Article.site_name,
                    Article.created_at
                )
            )
            article_data = result.first()

            try:
                session.commit()
                return {
                    "id": article_data.id,
                    "title": article_data.title,
                    "description": article_data.description,
                    "site_name": article_data.site_name,
                    "created_at": article_data.created_at
                }

            except IntegrityError as e:
                raise e
