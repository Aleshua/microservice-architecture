from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.article import Article


class ArticleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, article_id: int) -> Article | None:
        result = await self._session.execute(
            select(Article).where(Article.id == article_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Article | None:
        result = await self._session.execute(
            select(Article).where(Article.slug == slug)
        )
        return result.scalar_one_or_none()

    async def list(self, limit: int = 20, offset: int = 0) -> list[Article]:
        result = await self._session.execute(
            select(Article).order_by(Article.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self._session.execute(select(func.count(Article.id)))
        return result.scalar_one()

    async def create(self, article: Article) -> Article:
        self._session.add(article)
        await self._session.commit()
        await self._session.refresh(article)
        return article

    async def update(self, article: Article) -> Article:
        await self._session.commit()
        await self._session.refresh(article)
        return article

    async def delete(self, article: Article) -> None:
        await self._session.delete(article)
        await self._session.commit()
