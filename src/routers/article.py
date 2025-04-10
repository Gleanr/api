from fastapi import APIRouter, Depends
import newspaper
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation

from schemas.article import ArticleCreate, Article as ArticleResponse, ArticleSummaryList
from models.user import User
from models.article import Article
from models.associations import user_article
from utils.database import get_session
from utils.security import get_current_user
from utils.exceptions import raise_bad_request_exception, raise_internal_error_exception

router = APIRouter(
    prefix="/article",
    tags=["article"]
)


@router.post("/", response_model=ArticleResponse)
async def save_article(
    data: ArticleCreate,
    current_user: User = Depends(get_current_user)
):
    with get_session() as session:
        try:
            result = session.execute(
                sa.select(Article).where(Article.url == data.url)
            )
            existing_article = result.scalar_one_or_none()

            if existing_article:
                try:
                    session.execute(
                        sa.insert(user_article).values(
                            user_id=current_user.id,
                            article_id=existing_article.id
                        )
                    )
                    session.commit()

                except IntegrityError as e:
                    session.rollback()
                    if "already exists" in e.orig.args[0]:
                        return {"content_id": existing_article.id}

                    raise_internal_error_exception(f"Database constraint violated: {str(e)}")

                return {"content_id": existing_article.id}

        except IntegrityError as e:
            session.rollback()
            raise_internal_error_exception(f"Database constraint violated: {str(e)}")

    try:
        article = newspaper.article(data.url)

        with get_session() as session:
            try:
                result = session.execute(
                    sa.insert(Article).values(
                        url=article.url,
                        title=article.title,
                        content=article.text,
                        authors=article.authors,
                        published_date=article.publish_date,
                        top_image=article.top_image,
                        site_name = article.meta_site_name,
                        description = article.meta_description,
                    ).returning(Article.id)
                )

                article_id = result.scalar_one()

                session.execute(
                    sa.insert(user_article).values(
                        user_id=current_user.id,
                        article_id=article_id
                    )
                )

                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise_internal_error_exception(f"Database constraint violated: {str(e)}")

    except Exception as e:
        print(f"Error parsing article: {str(e)}")
        raise_bad_request_exception("Incorrect url")

    return {"content_id": article_id}


@router.get("/", response_model=ArticleSummaryList)
async def get_articles(current_user: User = Depends(get_current_user)):
    with get_session() as session:
        try:
            result = session.execute(
                sa.select(
                    Article.id,
                    Article.title,
                    Article.description,
                    Article.site_name,
                    Article.created_at
                )
                .join(user_article, Article.id == user_article.c.article_id)
                .where(user_article.c.user_id == current_user.id)
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

            return {"articles": articles}
        except Exception as e:
            raise_internal_error_exception(f"Failed to fetch articles: {str(e)}")
