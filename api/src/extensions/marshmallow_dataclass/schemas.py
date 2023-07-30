from __future__ import annotations

from dataclasses import asdict, field
from enum import Enum
from typing import Any, ClassVar, Type

from marshmallow import EXCLUDE, Schema
from marshmallow.validate import Range
from marshmallow_dataclass import dataclass


@dataclass
class Base:
    Schema: ClassVar[Type[Schema]] = Schema

    def dict(self) -> dict[str, Any]:
        result = asdict(self)
        return result

    class Meta:
        unknown = EXCLUDE


class Order(str, Enum):
    ASC = "ASC"
    asc = "asc"
    DESC = "DESC"
    desc = "desc"


class OrderBy(str, Enum):
    ...


@dataclass
class Query(Base):
    page: int | None = field(default=1, metadata={"validate": Range(min=1)})
    per_page: int | None = field(default=10, metadata={"validate": Range(min=0)})
    order: Order | None = field(default=Order.ASC)
    order_by: Type[OrderBy] | None = field(default=None)


@dataclass
class Pagination(Base):
    page: int | None
    per_page: int | None
    pages: int | None
    previous: int | None
    next: int | None
    total: int | None
    items: list[Type[Base]] | None
