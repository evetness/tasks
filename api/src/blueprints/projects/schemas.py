from dataclasses import dataclass, field
from typing import List

from marshmallow_dataclass import add_schema
from src.extensions.marshmallow_dataclass.schemas import Base, OrderBy, Pagination, Query


@dataclass
@add_schema
class ProjectBase(Base):
    name: str


@dataclass
@add_schema
class ProjectRead(ProjectBase):
    id: int


@dataclass
@add_schema
class ProjectWrite(ProjectBase):
    ...


class ProjectOrderBy(OrderBy):
    name = "name"


@dataclass
@add_schema
class ProjectQuery(Query):
    order_by: ProjectOrderBy = field(default=ProjectOrderBy.name)
    search: str | None = None


@dataclass
@add_schema
class ProjectPagination(Pagination):
    items: List[ProjectRead]


@dataclass
@add_schema
class Unpaid(Base):
    amount: float
    elapsed: str
    currency: str
