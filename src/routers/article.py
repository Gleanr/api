from fastapi import APIRouter
import newspaper
from schemas.article import ArticleCreate

router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)


@router.post("/save")
async def save_article(
    data: ArticleCreate
):
    # article = newspaper.article('https://edition.cnn.com/2025/04/04/style/steinway-tower-penthouse-110-million/index.html')
    # print(article.authors)
    # print(article.text)
    print(f"_URL_{data.url}")
    return {"URL": "SAVED"}
