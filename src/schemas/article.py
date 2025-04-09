from pydantic import BaseModel


class ArticleCreate(BaseModel):
    url: str


class Article(BaseModel):
    content_id: int
