from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.usecases import get_comment_usecases
from src.exceptions.article import ArticleNotFoundError
from src.exceptions.comment import CommentForbiddenError, CommentNotFoundError
from src.middleware.user import get_current_user
from src.models.user import User
from src.schemas.comment import CommentCreate, CommentListResponse, CommentResponse
from src.schemas.response import ApiResponse
from src.usecases.comment import CommentUseCases

router = APIRouter(prefix="/api/articles")


@router.post("/{slug}/comments", response_model=ApiResponse[CommentResponse], status_code=201)
async def add_comment(
    slug: str,
    data: CommentCreate,
    user: User = Depends(get_current_user),
    usecases: CommentUseCases = Depends(get_comment_usecases),
):
    try:
        comment = await usecases.add_comment(slug, data.body, user)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    return ApiResponse(
        message="comment created successfully",
        data=CommentResponse.model_validate(comment),
    )


@router.get("/{slug}/comments", response_model=ApiResponse[CommentListResponse])
async def get_comments(
    slug: str,
    usecases: CommentUseCases = Depends(get_comment_usecases),
):
    try:
        comments = await usecases.get_comments(slug)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    return ApiResponse(
        message="comments list",
        data=CommentListResponse(
            comments=[CommentResponse.model_validate(c) for c in comments],
        ),
    )


@router.delete("/{slug}/comments/{comment_id}", status_code=204)
async def delete_comment(
    slug: str,
    comment_id: int,
    user: User = Depends(get_current_user),
    usecases: CommentUseCases = Depends(get_comment_usecases),
):
    try:
        await usecases.delete_comment(slug, comment_id, user)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except CommentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except CommentForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
