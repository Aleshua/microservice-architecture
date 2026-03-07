from datetime import datetime

from pydantic import BaseModel, Field


class AuthorProfile(BaseModel):
    username: str
    bio: str | None = None
    image_url: str | None = None

    model_config = {"from_attributes": True}


class ArticleResponse(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tag_list: list[str] | None = Field(None, serialization_alias="tagList")
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")
    author: AuthorProfile

    model_config = {"from_attributes": True, "populate_by_name": True}


class ArticleListResponse(BaseModel):
    articles: list[ArticleResponse]

    model_config = {"populate_by_name": True}
