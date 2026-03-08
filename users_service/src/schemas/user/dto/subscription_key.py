from pydantic import BaseModel, field_validator


class SubscriptionKeyUpdate(BaseModel):
    subscription_key: str

    @field_validator("subscription_key")
    @classmethod
    def subscription_key_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("subscription_key must be a non-empty string")
        return v
