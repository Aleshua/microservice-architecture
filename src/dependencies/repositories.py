from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.repositories.article import ArticleRepository
from src.repositories.user import UserRepository


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


def get_article_repository(
    session: AsyncSession = Depends(get_session),
) -> ArticleRepository:
    return ArticleRepository(session)
