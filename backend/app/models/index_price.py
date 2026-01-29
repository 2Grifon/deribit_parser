from decimal import Decimal

from sqlmodel import Field, SQLModel

from app.core.utils.unix_now import unix_now


class IndexPrice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    index_name: str = Field(index=True)
    index_price: Decimal = Field(max_digits=10, decimal_places=2)
    timestamp: int = Field(default_factory=unix_now)
