from fastapi import Depends, HTTPException, status

from src.dependencies.repositories import get_user_repository
from src.middleware.auth import get_authenticated_user_id
from src.models.user import User
from src.repositories.user import UserRepository


async def get_current_user(
    user_id: int = Depends(get_authenticated_user_id),
    repository: UserRepository = Depends(get_user_repository),
) -> User:
    user = await repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not found",
        )
    return user
