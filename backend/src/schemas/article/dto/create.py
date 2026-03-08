from pydantic import BaseModel, Field


class ArticleCreate(BaseModel):
    title: str
    description: str
    body: str
    tag_list: list[str] | None = Field(None, alias="tagList")
