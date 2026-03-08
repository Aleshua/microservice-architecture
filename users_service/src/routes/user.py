from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.usecases import get_user_usecases
from src.exceptions.user import EmailOrUsernameTakenError, InvalidCredentialsError
from src.middleware.user import get_current_user
from src.models.user import User
from src.schemas.response import ApiResponse
from src.schemas.user import AuthResponse, SubscriptionKeyUpdate, TokenResponse, UserCreate, UserLogin, UserResponse, UserUpdate
from src.usecases.user import UserUseCases

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("", response_model=ApiResponse[AuthResponse], status_code=201)
async def register(
    data: UserCreate,
    usecases: UserUseCases = Depends(get_user_usecases),
):
    try:
        user, token = await usecases.register(data)
    except EmailOrUsernameTakenError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    user_dict = UserResponse.model_validate(user).model_dump()
    user_dict["token"] = token
    return ApiResponse(
        message="user registered successfully",
        data=AuthResponse(**user_dict),
    )


@router.post("/login", response_model=ApiResponse[TokenResponse])
async def login(
    data: UserLogin,
    usecases: UserUseCases = Depends(get_user_usecases),
):
    try:
        token = await usecases.login(data)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    return ApiResponse(
        message="login successful",
        data=TokenResponse(token=token),
    )


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_current(
    user: User = Depends(get_current_user),
):
    return ApiResponse(
        message="user profile",
        data=UserResponse.model_validate(user),
    )


@router.put("/me/subscription-key", response_model=ApiResponse[UserResponse])
async def update_subscription_key(
    data: SubscriptionKeyUpdate,
    user: User = Depends(get_current_user),
    usecases: UserUseCases = Depends(get_user_usecases),
):
    user = await usecases.update_subscription_key(user, data)
    return ApiResponse(
        message="subscription key updated successfully",
        data=UserResponse.model_validate(user),
    )


@router.put("/me", response_model=ApiResponse[UserResponse])
async def update(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    usecases: UserUseCases = Depends(get_user_usecases),
):
    try:
        user = await usecases.update(user, data)
    except EmailOrUsernameTakenError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    return ApiResponse(
        message="user updated successfully",
        data=UserResponse.model_validate(user),
    )
