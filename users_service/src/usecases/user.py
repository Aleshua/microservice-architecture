from src.exceptions.user import (
    EmailOrUsernameTakenError,
    EmailTakenError,
    InvalidCredentialsError,
    UsernameTakenError,
)
from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import SubscriptionKeyUpdate, UserCreate, UserLogin, UserUpdate
from src.services.password import PasswordService
from src.services.token import TokenService


class UserUseCases:
    def __init__(
        self,
        repository: UserRepository,
        password_service: PasswordService,
        token_service: TokenService,
    ) -> None:
        self._repo = repository
        self._password = password_service
        self._token = token_service

    async def register(self, data: UserCreate) -> tuple[User, str]:
        existing = await self._repo.get_by_email_or_username(data.email, data.username)
        if existing is not None:
            raise EmailOrUsernameTakenError()

        user = User(
            email=data.email,
            username=data.username,
            password_hash=self._password.hash(data.password),
        )
        user = await self._repo.create(user)
        token = self._token.create(user.id)

        return user, token

    async def login(self, data: UserLogin) -> str:
        user = await self._repo.get_by_email(data.email)

        if user is None or not self._password.verify(data.password, user.password_hash):
            raise InvalidCredentialsError()

        return self._token.create(user.id)

    async def update(self, user: User, data: UserUpdate) -> User:
        if data.email is not None and data.email != user.email:
            if await self._repo.get_by_email(data.email) is not None:
                raise EmailTakenError()
            user.email = data.email

        if data.username is not None and data.username != user.username:
            if await self._repo.get_by_username(data.username) is not None:
                raise UsernameTakenError()
            user.username = data.username

        if data.password is not None:
            user.password_hash = self._password.hash(data.password)

        if data.bio is not None:
            user.bio = data.bio

        if data.image_url is not None:
            user.image_url = data.image_url

        user = await self._repo.update(user)

        return user

    async def update_subscription_key(self, user: User, data: SubscriptionKeyUpdate) -> User:
        user.subscription_key = data.subscription_key
        user = await self._repo.update(user)
        return user
