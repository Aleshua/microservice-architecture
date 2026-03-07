from pydantic import BaseModel, Field


class ArticleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    body: str | None = None
    tag_list: list[str] | None = Field(None, alias="tagList")
