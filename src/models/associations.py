from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.user import metadata, User
from models.article import Article

user_article = Table(
    "user_article",
    metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("article_id", Integer, ForeignKey("article.id"), primary_key=True)
)

User.articles = relationship("Article", secondary=user_article, back_populates="users")
Article.users = relationship("User", secondary=user_article, back_populates="articles")
