from fastapi import APIRouter, Depends

from domain.daos.article_db import ArticleDbDAO
from domain.daos.article_web import ArticleWebDAO
from domain.usecases.get_article_usecase import GetArticleUsecase
from domain.usecases.get_articles_list_usecase import GetArticlesListUsecase
from domain.usecases.save_aricle_usecase import SaveArticleUsecase
from schemas.article import ArticleCreate, NewArticleSummary as ArticleResponse, ArticleSummaryList, ArticleDetail
from models.user import User
from utils.security import get_current_user

router = APIRouter(
    prefix="/article",
    tags=["article"]
)


@router.post("/", response_model=ArticleResponse)
async def save_article(
        data: ArticleCreate,
        current_user: User = Depends(get_current_user)
):
    article_db_dao = ArticleDbDAO()
    article_web_dao = ArticleWebDAO()
    usecase = SaveArticleUsecase(article_db_dao, article_web_dao)
    article = usecase.execute(url=data.url, user_id=current_user.id)
    return {"new_article": article}


@router.get("/", response_model=ArticleSummaryList)
async def get_articles(current_user: User = Depends(get_current_user)):
    article_db_dao = ArticleDbDAO()
    usecase = GetArticlesListUsecase(article_db_dao)
    articles = usecase.execute(user_id=current_user.id)
    return {"articles": articles}

@router.get("/{id}", response_model=ArticleDetail)
async def get_article_by_id(
        id: int,
        current_user: User = Depends(get_current_user)
):
    article_db_dao = ArticleDbDAO()
    usecase = GetArticleUsecase(article_db_dao)

    return usecase.execute(user_id=current_user.id, article_id=id)