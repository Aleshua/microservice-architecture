from datetime import datetime

from pydantic import BaseModel, Field


class ArticleResponse(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tag_list: list[str] | None = Field(None, serialization_alias="tagList")
    author_id: int
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


class ArticleListResponse(BaseModel):
    articles: list[ArticleResponse]

    model_config = {"populate_by_name": True}
