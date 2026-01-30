from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.core.db import SessionDep
from app.models.index_price import IndexPrice

index_router = APIRouter(prefix="/prices", tags=["prices"])


@index_router.get("/last", response_model=IndexPrice)
async def get_last_price(session: SessionDep, ticker: str = Query(...)):
    """Получает последнюю цену по тикеру."""
    statement = (
        select(IndexPrice)
        .where(IndexPrice.index_name.ilike(f"%{ticker}%"))
        .order_by(IndexPrice.timestamp.desc())
    )
    result = await session.exec(statement)
    last_index_price: IndexPrice = result.first()

    if not last_index_price:
        raise HTTPException(status_code=404, detail="Price not found")

    return last_index_price


@index_router.get("/", response_model=List[IndexPrice])  # TODO: пагинация
async def get_prices(
    session: SessionDep,
    ticker: str = Query(...),
    date_from: Optional[int] = Query(None, description="Unix timestamp (inclusive)"),
    date_to: Optional[int] = Query(None, description="Unix timestamp (inclusive)"),
):
    """Получает список цен по тикеру и опциональному диапазону дат."""
    statement = select(IndexPrice).where(IndexPrice.index_name.ilike(f"%{ticker}%"))

    if date_from is not None:
        statement = statement.where(IndexPrice.timestamp >= date_from)
    if date_to is not None:
        statement = statement.where(IndexPrice.timestamp <= date_to)

    statement = statement.order_by(IndexPrice.timestamp.desc())
    result = await session.exec(statement)

    return result.all()
