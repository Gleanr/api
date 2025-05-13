import newspaper

from domain.entities import ArticleEntity
from utils.exceptions import raise_bad_request_exception


class ArticleWebDAO:
    def get(self, url: str) -> ArticleEntity:
        try:
            article = newspaper.article(url)

            return ArticleEntity(
                url=article.url,
                title=article.title,
                content=article.text,
                authors=article.authors,
                published_date=article.publish_date,
                top_image=article.top_image,
                site_name=article.meta_site_name,
                description=article.meta_description
            )

        except Exception as e:
            print(f"Error parsing article: {str(e)}")
            raise_bad_request_exception("Incorrect url")
