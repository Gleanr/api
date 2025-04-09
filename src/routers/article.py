from fastapi import APIRouter, Depends
import newspaper
from schemas.article import ArticleCreate
from utils.security import get_current_user
from models.user import User

router = APIRouter(
    prefix="/article",
    tags=["article"]
)


@router.post("/")
async def save_article(
    data: ArticleCreate,
    current_user: User = Depends(get_current_user)
):
    print(data.url, current_user.id, current_user.email)
    article = newspaper.article(data.url)
    print(article.title)
    print(article.authors)

    return {"URL": "SAVED"}
