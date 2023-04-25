from __future__ import annotations

from dataclasses import field
from enum import Enum
from typing import ClassVar, Type

from marshmallow import Schema
from marshmallow.validate import Range
from marshmallow_dataclass import dataclass


@dataclass
class Base:
    Schema: ClassVar[Type[Schema]] = Schema

    def dict(self, *args, **kwargs):
        values = self.Schema(*args, **kwargs).dump(self)
        result = {}
        for key, value in values.items():
            if value is None:
                continue
            result.setdefault(key, value)

        return result


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
    order: Order | None = Order.ASC
    order_by: Type[OrderBy] | None = None

    @property
    def limit(self) -> int | None:
        if self.per_page == 0:
            return None
        return self.per_page

    @property
    def offset(self) -> int | None:
        if self.per_page:
            return (self.page - 1) * self.per_page
        return None


@dataclass
class Pagination(Base):
    page: int | None
    per_page: int | None
    pages: int | None
    previous: int | None
    next: int | None
    total: int | None
    items: list[Type[Base]] | None
