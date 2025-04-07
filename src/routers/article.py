from fastapi import APIRouter, Depends
import newspaper
from schemas.article import ArticleCreate
from utils.security import get_current_user
from models.users import User

router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)


@router.post("/save")
async def save_article(
    data: ArticleCreate,
    current_user: User = Depends(get_current_user)
):
    print(f"_URL_{data.url}")
    return {"URL": "SAVED"}
