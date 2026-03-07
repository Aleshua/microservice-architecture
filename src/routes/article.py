import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.dependencies.usecases import get_article_usecases
from src.exceptions.article import ArticleForbiddenError, ArticleNotFoundError
from src.middleware.user import get_current_user
from src.models.user import User
from src.schemas.article import ArticleCreate, ArticleListResponse, ArticleResponse, ArticleUpdate
from src.schemas.response import ApiResponse, Meta
from src.usecases.article import ArticleUseCases

router = APIRouter(prefix="/api/articles")
logger = logging.getLogger(__name__)


@router.post("", response_model=ApiResponse[ArticleResponse], status_code=201)
async def create_article(
    data: ArticleCreate,
    user: User = Depends(get_current_user),
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    try:
        article = await usecases.create(data, user)
        return ApiResponse(
            message="article created successfully",
            data=ArticleResponse.model_validate(article),
        )
    except Exception:
        logger.exception("failed to create article")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to create article",
        )


@router.get("", response_model=ApiResponse[ArticleListResponse])
async def list_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    try:
        offset = (page - 1) * limit
        articles, count = await usecases.list(limit=limit, offset=offset)
        return ApiResponse(
            message="articles list",
            data=ArticleListResponse(
                articles=[ArticleResponse.model_validate(a) for a in articles],
            ),
            meta=Meta(total=count, page=page, per_page=limit),
        )
    except Exception:
        logger.exception("failed to list articles")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to list articles",
        )


@router.get("/{slug}", response_model=ApiResponse[ArticleResponse])
async def get_article(
    slug: str,
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    try:
        article = await usecases.get_by_slug(slug)
        return ApiResponse(
            message="article details",
            data=ArticleResponse.model_validate(article),
        )
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except Exception:
        logger.exception("failed to get article")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to get article",
        )


@router.put("/{slug}", response_model=ApiResponse[ArticleResponse])
async def update_article(
    slug: str,
    data: ArticleUpdate,
    user: User = Depends(get_current_user),
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    try:
        article = await usecases.update(slug, data, user)
        return ApiResponse(
            message="article updated successfully",
            data=ArticleResponse.model_validate(article),
        )
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except ArticleForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
    except Exception:
        logger.exception("failed to update article")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to update article",
        )


@router.delete("/{slug}", status_code=204)
async def delete_article(
    slug: str,
    user: User = Depends(get_current_user),
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    try:
        await usecases.delete(slug, user)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except ArticleForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
    except Exception:
        logger.exception("failed to delete article")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to delete article",
        )
