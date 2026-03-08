from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_URL: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
