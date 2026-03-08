from pydantic import BaseModel


class SubscribeRequest(BaseModel):
    target_user_id: int
