from src.exceptions.user import CannotSubscribeToSelfError, TargetUserNotFoundError
from src.repositories.subscriber import SubscriberRepository
from src.repositories.user import UserRepository
from src.schemas.user import SubscribeRequest


class SubscriptionUseCases:
    def __init__(
        self,
        user_repository: UserRepository,
        subscriber_repository: SubscriberRepository,
    ) -> None:
        self._user_repo = user_repository
        self._subscriber_repo = subscriber_repository

    async def subscribe(self, subscriber_id: int, data: SubscribeRequest) -> None:
        if data.target_user_id == subscriber_id:
            raise CannotSubscribeToSelfError()

        target = await self._user_repo.get_by_id(data.target_user_id)
        if target is None:
            raise TargetUserNotFoundError()

        await self._subscriber_repo.subscribe(
            subscriber_id=subscriber_id, author_id=data.target_user_id
        )
