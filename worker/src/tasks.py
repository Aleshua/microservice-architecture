import logging
import os

import requests
from sqlalchemy import BigInteger, Column, DateTime, String, Text, create_engine, func, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.celery_app import app

logger = logging.getLogger(__name__)

USERS_DATABASE_URL = os.getenv(
    "USERS_DATABASE_URL", "postgresql://postgres:postgres@users-db:5432/users"
)
PUSH_URL = os.getenv("PUSH_URL", "http://push-notificator:8000/api/v1/notify")

engine = create_engine(USERS_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


@app.task(
    name="notify_followers",
    bind=True,
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    retry_backoff_max=300,
    max_retries=5,
)
def notify_followers(self, author_id: int, post_id: int, title: str = "") -> None:
    logger.info(
        "Received task: author_id=%s, post_id=%s, title=%s",
        author_id, post_id, title,
    )

    truncated_title = title[:10] + "..." if len(title) > 10 else title

    with SessionLocal() as session:
        rows = session.execute(
            text(
                """
                SELECT s.subscriber_id, u.subscription_key
                FROM subscribers s
                JOIN users u ON u.id = s.subscriber_id
                WHERE s.author_id = :author_id
                """
            ),
            {"author_id": author_id},
        ).fetchall()

        if not rows:
            logger.info(
                "No subscribers for author_id=%s, post_id=%s", author_id, post_id
            )
            return

        for subscriber_id, subscription_key in rows:
            if not subscription_key:
                logger.warning(
                    "Empty subscription_key: author_id=%s, subscriber_id=%s, post_id=%s",
                    author_id, subscriber_id, post_id,
                )
                continue

            already_sent = session.execute(
                text(
                    """
                    SELECT 1 FROM notifications_sent
                    WHERE subscriber_id = :subscriber_id AND post_id = :post_id
                    """
                ),
                {"subscriber_id": subscriber_id, "post_id": post_id},
            ).fetchone()

            if already_sent:
                logger.info(
                    "Already notified: subscriber_id=%s, post_id=%s",
                    subscriber_id, post_id,
                )
                continue

            message = f"Пользователь {author_id} выпустил новый пост: {truncated_title}"

            logger.info(
                "Sending notification: author_id=%s, subscriber_id=%s, post_id=%s",
                author_id, subscriber_id, post_id,
            )

            response = requests.post(
                PUSH_URL,
                json={"message": message},
                headers={"Authorization": f"Bearer {subscription_key}"},
                timeout=5,
            )
            response.raise_for_status()

            session.execute(
                text(
                    """
                    INSERT INTO notifications_sent (subscriber_id, post_id)
                    VALUES (:subscriber_id, :post_id)
                    ON CONFLICT (subscriber_id, post_id) DO NOTHING
                    """
                ),
                {"subscriber_id": subscriber_id, "post_id": post_id},
            )
            session.commit()

            logger.info(
                "Notification sent: author_id=%s, subscriber_id=%s, post_id=%s",
                author_id, subscriber_id, post_id,
            )
