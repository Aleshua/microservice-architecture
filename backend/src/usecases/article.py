import uuid

from slugify import slugify

from src.exceptions.article import ArticleForbiddenError, ArticleNotFoundError
from src.models.article import Article
from src.repositories.article import ArticleRepository
from src.schemas.article import ArticleCreate, ArticleUpdate


class ArticleUseCases:
    def __init__(self, repository: ArticleRepository) -> None:
        self._repo = repository

    async def _generate_slug(self, title: str) -> str:
        slug = slugify(title)
        existing = await self._repo.get_by_slug(slug)
        if existing is not None:
            slug = f"{slug}-{uuid.uuid4().hex[:8]}"
        return slug

    async def create(self, data: ArticleCreate, author_id: int) -> Article:
        slug = await self._generate_slug(data.title)
        article = Article(
            slug=slug,
            title=data.title,
            description=data.description,
            body=data.body,
            tag_list=data.tag_list,
            author_id=author_id,
        )
        article = await self._repo.create(article)
        return article

    async def list(self, limit: int = 20, offset: int = 0) -> tuple[list[Article], int]:
        articles = await self._repo.list(limit=limit, offset=offset)
        count = await self._repo.count()
        return articles, count

    async def get_by_slug(self, slug: str) -> Article:
        article = await self._repo.get_by_slug(slug)
        if article is None:
            raise ArticleNotFoundError()
        return article

    async def update(self, slug: str, data: ArticleUpdate, user_id: int) -> Article:
        article = await self._repo.get_by_slug(slug)
        if article is None:
            raise ArticleNotFoundError()
        if article.author_id != user_id:
            raise ArticleForbiddenError()

        if data.title is not None:
            article.title = data.title
            article.slug = await self._generate_slug(data.title)

        if data.description is not None:
            article.description = data.description

        if data.body is not None:
            article.body = data.body

        if data.tag_list is not None:
            article.tag_list = data.tag_list

        article = await self._repo.update(article)
        return article

    async def delete(self, slug: str, user_id: int) -> None:
        article = await self._repo.get_by_slug(slug)
        if article is None:
            raise ArticleNotFoundError()
        if article.author_id != user_id:
            raise ArticleForbiddenError()

        await self._repo.delete(article)
