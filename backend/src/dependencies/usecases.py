from fastapi import Depends

from src.dependencies.repositories import get_article_repository, get_comment_repository
from src.repositories.article import ArticleRepository
from src.repositories.comment import CommentRepository
from src.usecases.article import ArticleUseCases
from src.usecases.comment import CommentUseCases


def get_article_usecases(
    repository: ArticleRepository = Depends(get_article_repository),
) -> ArticleUseCases:
    return ArticleUseCases(repository)


def get_comment_usecases(
    repository: CommentRepository = Depends(get_comment_repository),
    article_repository: ArticleRepository = Depends(get_article_repository),
) -> CommentUseCases:
    return CommentUseCases(repository, article_repository)
