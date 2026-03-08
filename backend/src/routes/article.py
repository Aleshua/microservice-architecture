from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.celery_app import celery
from src.dependencies.usecases import get_article_usecases
from src.exceptions.article import ArticleForbiddenError, ArticleNotFoundError
from src.middleware.auth import get_authenticated_user_id
from src.schemas.article import ArticleCreate, ArticleListResponse, ArticleResponse, ArticleUpdate
from src.schemas.response import ApiResponse, Meta
from src.usecases.article import ArticleUseCases

router = APIRouter(prefix="/api/articles", tags=["Articles"])


@router.post("", response_model=ApiResponse[ArticleResponse], status_code=201)
async def create_article(
    data: ArticleCreate,
    user_id: int = Depends(get_authenticated_user_id),
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    article = await usecases.create(data, user_id)
    celery.send_task(
        "notify_followers",
        kwargs={"author_id": user_id, "post_id": article.id, "title": article.title},
    )
    return ApiResponse(
        message="article created successfully",
        data=ArticleResponse.model_validate(article),
    )


@router.get("", response_model=ApiResponse[ArticleListResponse])
async def list_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    offset = (page - 1) * limit
    articles, count = await usecases.list(limit=limit, offset=offset)
    return ApiResponse(
        message="articles list",
        data=ArticleListResponse(
            articles=[ArticleResponse.model_validate(a) for a in articles],
        ),
        meta=Meta(total=count, page=page, per_page=limit),
    )


@router.get("/{slug}", response_model=ApiResponse[ArticleResponse])
async def get_article(
    slug: str,
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    try:
        article = await usecases.get_by_slug(slug)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    return ApiResponse(
        message="article details",
        data=ArticleResponse.model_validate(article),
    )


@router.put("/{slug}", response_model=ApiResponse[ArticleResponse])
async def update_article(
    slug: str,
    data: ArticleUpdate,
    user_id: int = Depends(get_authenticated_user_id),
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    try:
        article = await usecases.update(slug, data, user_id)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except ArticleForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
    return ApiResponse(
        message="article updated successfully",
        data=ArticleResponse.model_validate(article),
    )


@router.delete("/{slug}", status_code=204)
async def delete_article(
    slug: str,
    user_id: int = Depends(get_authenticated_user_id),
    usecases: ArticleUseCases = Depends(get_article_usecases),
):
    try:
        await usecases.delete(slug, user_id)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except ArticleForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
