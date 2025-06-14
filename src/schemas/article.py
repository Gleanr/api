from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ArticleCreate(BaseModel):
    url: str


class Article(BaseModel):
    content_id: int


class ArticleSummary(BaseModel):
    id: int
    title: str
    site_name: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime


class ArticleDetail(ArticleSummary):
    url: str
    content: str
    authors: Optional[list[str]] = None
    published_date: Optional[str] = None
    top_image: Optional[str] = None


class ArticleList(BaseModel):
    articles: List[ArticleDetail]


class ArticleSummaryList(BaseModel):
    articles: List[ArticleSummary]

class NewArticleSummary(BaseModel):
    new_article: ArticleSummary
