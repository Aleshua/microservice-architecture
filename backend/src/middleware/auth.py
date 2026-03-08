from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.dependencies.security import get_token_service
from src.services.token import TokenService

bearer_scheme = HTTPBearer()


def get_authenticated_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    token_service: TokenService = Depends(get_token_service),
) -> int:
    user_id = token_service.decode(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expired token",
        )
    return user_id
