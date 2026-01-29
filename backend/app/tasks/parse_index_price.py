from decimal import Decimal
from celery import shared_task
from sqlmodel import Session

from app.core.api_manager.base import ApiError
from app.core.db import sync_engine
from app.integrations.deribit_api_manager import DeribitAPIManager
from app.models.index_price import IndexPrice


@shared_task(
    autoretry_for=(ApiError,),
    retry_kwargs={"max_retries": 3, "countdown": 10},
)
def parse_index_price():
    api_manager = DeribitAPIManager()
    btc_index_price = api_manager.get_index_price(currency="btc")
    eth_index_price = api_manager.get_index_price(currency="eth")

    with Session(sync_engine) as session:
        session.add_all(
            [
                IndexPrice(index_name="btc_usd", index_price=Decimal(btc_index_price)),
                IndexPrice(index_name="eth_usd", index_price=Decimal(eth_index_price)),
            ]
        )
        session.commit()
