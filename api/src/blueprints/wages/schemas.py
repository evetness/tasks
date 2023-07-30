from dataclasses import dataclass, field
import datetime
from typing import List

from marshmallow_dataclass import add_schema

from src.extensions.marshmallow_dataclass.schemas import Base, OrderBy, Query, Pagination


@dataclass
@add_schema
class WageBase(Base):
    date: datetime.date
    amount: int
    currency: str


@dataclass
@add_schema
class WageRead(WageBase):
    id: int


@dataclass
@add_schema
class WageCreate(WageBase):
    project_id: int


@dataclass
@add_schema
class WageUpdate(WageBase):
    ...


class WageOrderBy(OrderBy):
    date = "date"
    amount = "amount"
    currency = "currency"


@dataclass
@add_schema
class WageQuery(Query):
    order_by: WageOrderBy = field(default=WageOrderBy.date)
    project_id: int = field(default=0, metadata={"required": True})


@dataclass
@add_schema
class WagePagination(Pagination):
    items: List[WageRead]
