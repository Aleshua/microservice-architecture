from datetime import datetime

from pydantic import BaseModel


class AuthResponse(BaseModel):
    email: str
    username: str
    bio: str | None = None
    image_url: str | None = None
    token: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
