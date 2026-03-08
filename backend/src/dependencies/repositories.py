from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.repositories.article import ArticleRepository
from src.repositories.comment import CommentRepository


def get_article_repository(
    session: AsyncSession = Depends(get_session),
) -> ArticleRepository:
    return ArticleRepository(session)


def get_comment_repository(
    session: AsyncSession = Depends(get_session),
) -> CommentRepository:
    return CommentRepository(session)
