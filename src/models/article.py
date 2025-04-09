from sqlalchemy import Column, Integer, String, Text, ARRAY
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from models.user import Base


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    authors = Column(ARRAY(String), nullable=True)
    published_date = Column(String, nullable=True)
    top_image = Column(String, nullable=True)
    site_name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
