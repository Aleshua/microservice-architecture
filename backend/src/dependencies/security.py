from functools import lru_cache

from src.config import settings
from src.services.token import TokenService


@lru_cache
def get_token_service() -> TokenService:
    return TokenService(
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
