from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserEntity(BaseModel):
    id: Optional[int] = None
    email: str
    password: str
    created_at: Optional[datetime] = None


class ArticleEntity(BaseModel):
    id: Optional[int] = None
    url: str = Field()
    title: str
    content: str
    site_name: Optional[str] = None
    description: Optional[str] = None
    authors: Optional[list[str]] = None
    top_image: Optional[str] = None
    published_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
