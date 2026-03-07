from fastapi import Depends

from src.dependencies.repositories import get_article_repository, get_comment_repository, get_user_repository
from src.dependencies.security import get_password_service, get_token_service
from src.repositories.article import ArticleRepository
from src.repositories.comment import CommentRepository
from src.repositories.user import UserRepository
from src.services.password import PasswordService
from src.services.token import TokenService
from src.usecases.article import ArticleUseCases
from src.usecases.comment import CommentUseCases
from src.usecases.user import UserUseCases


def get_user_usecases(
    repository: UserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),
    token_service: TokenService = Depends(get_token_service),
) -> UserUseCases:
    return UserUseCases(repository, password_service, token_service)


def get_article_usecases(
    repository: ArticleRepository = Depends(get_article_repository),
) -> ArticleUseCases:
    return ArticleUseCases(repository)


def get_comment_usecases(
    repository: CommentRepository = Depends(get_comment_repository),
    article_repository: ArticleRepository = Depends(get_article_repository),
) -> CommentUseCases:
    return CommentUseCases(repository, article_repository)
