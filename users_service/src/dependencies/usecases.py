from fastapi import Depends

from src.dependencies.repositories import get_subscriber_repository, get_user_repository
from src.dependencies.security import get_password_service, get_token_service
from src.repositories.subscriber import SubscriberRepository
from src.repositories.user import UserRepository
from src.services.password import PasswordService
from src.services.token import TokenService
from src.usecases.subscription import SubscriptionUseCases
from src.usecases.user import UserUseCases


def get_user_usecases(
    repository: UserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),
    token_service: TokenService = Depends(get_token_service),
) -> UserUseCases:
    return UserUseCases(repository, password_service, token_service)


def get_subscription_usecases(
    user_repository: UserRepository = Depends(get_user_repository),
    subscriber_repository: SubscriberRepository = Depends(get_subscriber_repository),
) -> SubscriptionUseCases:
    return SubscriptionUseCases(user_repository, subscriber_repository)
