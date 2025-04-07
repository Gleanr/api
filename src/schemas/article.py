from pydantic import BaseModel, HttpUrl


class ArticleCreate(BaseModel):
    url: HttpUrl
