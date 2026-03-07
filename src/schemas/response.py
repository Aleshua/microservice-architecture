from typing import Generic, TypeVar

from pydantic import BaseModel, model_serializer

T = TypeVar("T")


class Links(BaseModel):
    self: str | None = None
    next: str | None = None
    prev: str | None = None


class Meta(BaseModel):
    total: int | None = None
    page: int | None = None
    per_page: int | None = None


class ApiResponse(BaseModel, Generic[T]):
    message: str
    data: T | None = None
    links: Links | None = None
    meta: Meta | None = None

    @model_serializer
    def serialize(self) -> dict:
        result: dict = {"message": self.message, "data": self.data}
        if self.links is not None:
            result["links"] = self.links
        if self.meta is not None:
            result["meta"] = self.meta
        return result


class ErrorResponse(BaseModel):
    message: str
    detail: str | None = None
