from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comment import Comment


class CommentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, comment_id: int) -> Comment | None:
        result = await self._session.execute(
            select(Comment).where(Comment.id == comment_id)
        )
        return result.scalar_one_or_none()

    async def list_by_article_id(self, article_id: int) -> list[Comment]:
        result = await self._session.execute(
            select(Comment)
            .where(Comment.article_id == article_id)
            .order_by(Comment.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(self, comment: Comment) -> Comment:
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def delete(self, comment: Comment) -> None:
        await self._session.delete(comment)
        await self._session.commit()
