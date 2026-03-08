from celery import Celery

from src.config import settings

celery = Celery("worker", broker=settings.REDIS_URL)
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
