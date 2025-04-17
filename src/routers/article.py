from fastapi import APIRouter, Depends
import newspaper
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation

from daos.article import ArticleDAO
from schemas.article import ArticleCreate, Article as ArticleResponse, ArticleSummaryList, ArticleDetail
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
    article_dao = ArticleDAO()

    try:
        try:
            existing_article = article_dao.get_by_url(data.url)
            article_dao.insert_user_article(current_user.id, existing_article.id)

            return {"content_id": existing_article.id}

        except ArticleDAO.UserArticleAlreadyExistsError:
            return {"content_id": existing_article.id}

        except ArticleDAO.ArticleNotFoundError:
            try:
                article = newspaper.article(data.url)
            except Exception as e:
                print(f"Error parsing article: {str(e)}")
                raise_bad_request_exception("Incorrect url")

            article_data = {
                "url": article.url,
                "title": article.title,
                "content": article.text,
                "authors": article.authors,
                "published_date": article.publish_date,
                "top_image": article.top_image,
                "site_name": article.meta_site_name,
                "description": article.meta_description,
            }

            new_article_id = article_dao.insert_article(article_data)
            article_dao.insert_user_article(current_user.id, new_article_id)

            return {"content_id": new_article_id}

    except IntegrityError as e:
        raise_internal_error_exception(f"Database constraint violated: {str(e)}")


@router.get("/", response_model=ArticleSummaryList)
async def get_articles(current_user: User = Depends(get_current_user)):
    article_dao = ArticleDAO()

    try:
        articles = article_dao.get_list(current_user.id)

        return {"articles": articles}
    except Exception as e:
            raise_internal_error_exception(str(e))


@router.get("/{id}", response_model=ArticleDetail)
async def get_article_by_id(
        id: int,
        current_user: User = Depends(get_current_user)
):
    article_dao = ArticleDAO()

    try:
        return article_dao.get_details(current_user.id, id)

    except ArticleDAO.ArticleNotFoundError:
        raise_bad_request_exception("Article not found or not accessible")
    except Exception as e:
        raise_internal_error_exception(str(e))
