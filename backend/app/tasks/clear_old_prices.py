from datetime import datetime, timezone, timedelta

from celery import shared_task
from sqlmodel import Session, delete

from app.core.db import sync_engine
from app.models.index_price import IndexPrice


@shared_task
def clear_old_prices():
    """Удаляет данные таблицы index_price с timestamp старше 30 дней."""
    threshold = int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp())
    with Session(sync_engine) as session:
        statement = delete(IndexPrice).where(IndexPrice.timestamp < threshold)
        session.exec(statement)
        session.commit()
