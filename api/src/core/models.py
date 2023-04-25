from __future__ import annotations
from math import ceil

from typing import Optional, TypeVar
from apiflask import HTTPError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Field, select, func

from src.extensions import db


class Base(db.Model):
    __abstract__ = True

    id: Optional[int] = Field(default=None, primary_key=True)

    def save(self, raise_error=True) -> TBase:
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if raise_error:
                raise HTTPError(500, "DATABASE_SAVE_ERROR")
        return self

    def update(self, **kwargs) -> TBase:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def delete(self, raise_error=True) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            if raise_error:
                raise HTTPError(500, "DATABASE_DELETE_ERROR")


TBase = TypeVar("TBase", bound=Base)


class Pagination:
    def __init__(self, page: int | None, per_page: int | None, query: select):
        self._page = page
        self._per_page = per_page
        self._query = query

    @property
    def page(self) -> int:
        return self._page or 1

    @property
    def per_page(self) -> int:
        return self._per_page or self.total

    @property
    def items(self) -> list:
        return db.session.scalars(self._query).all()

    @property
    def total(self) -> int:
        return db.session.scalar(select(func.count()).select_from(self._query.subquery()))

    @property
    def pages(self) -> int:
        if self.per_page == 0:
            return 1
        return int(ceil(self.total / float(self.per_page)))

    @property
    def previous(self) -> int:
        if self.page <= 1:
            return 0
        return self.page - 1

    @property
    def next(self) -> int:
        if self.page >= self.pages:
            return 0
        return self.page + 1
