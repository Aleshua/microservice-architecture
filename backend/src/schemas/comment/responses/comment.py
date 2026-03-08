from datetime import datetime

from pydantic import BaseModel, Field


class CommentResponse(BaseModel):
    id: int
    body: str
    author_id: int
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


class CommentListResponse(BaseModel):
    comments: list[CommentResponse]

    model_config = {"populate_by_name": True}
