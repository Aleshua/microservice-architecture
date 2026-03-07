from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas.article.responses.article import AuthorProfile


class CommentResponse(BaseModel):
    id: int
    body: str
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")
    author: AuthorProfile

    model_config = {"from_attributes": True, "populate_by_name": True}


class CommentListResponse(BaseModel):
    comments: list[CommentResponse]

    model_config = {"populate_by_name": True}
