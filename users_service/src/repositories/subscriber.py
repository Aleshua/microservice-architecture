from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.subscriber import Subscriber


class SubscriberRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def subscribe(self, subscriber_id: int, author_id: int) -> None:
        stmt = (
            pg_insert(Subscriber)
            .values(subscriber_id=subscriber_id, author_id=author_id)
            .on_conflict_do_nothing(constraint="uq_subscriber_author")
        )
        await self._session.execute(stmt)
        await self._session.commit()
