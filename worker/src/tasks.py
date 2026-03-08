import logging

from src.celery_app import app

logger = logging.getLogger(__name__)


@app.task(name="notify_followers")
def notify_followers(author_id: int, post_id: int) -> None:
    logger.info("Received task: author_id=%s, post_id=%s", author_id, post_id)
