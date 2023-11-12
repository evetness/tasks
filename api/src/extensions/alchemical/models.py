from __future__ import annotations
from math import ceil

from typing import Optional, TypeVar
from loguru import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import lazyload
from sqlmodel import Field, select, func

from src.extensions import db
from src.extensions.alchemical.errors import DatabaseDeleteError, DatabaseInsertError


class Base(db.Model):
    __abstract__ = True

    id: Optional[int] = Field(default=None, primary_key=True)

    def save(self) -> TBase:
        try:
            db.session.add(self)
            db.session.commit()
            db.session.refresh(self)
        except IntegrityError as e:
            logger.warning(f"{self.__class__.__name__}: sqlalchemy error: {e}")
            db.session.rollback()
            raise DatabaseInsertError
        return self

    def update(self, **kwargs) -> "Base":
        logger.debug(f"{self.__class__.__name__}: {kwargs}")

        for key, value in kwargs.items():
            if key == "id" or key == "uuid":
                continue
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            logger.warning(f"{self.__class__.__name__}: sqlalchemy error: {e}")
            db.session.rollback()
            raise DatabaseDeleteError

TBase = TypeVar("TBase", bound=Base)


class Pagination:
    def __init__(self, page: int | None, per_page: int | None, statement: select):
        self._page = page
        self._per_page = per_page
        self._statement = statement
        self.items = self.read_items()
        self.total = self.read_total()

    def read_items(self):
        statement = self._statement.limit(self._limit).offset(self._offset)
        logger.debug(statement)
        return db.session.scalars(statement).unique().all()

    def read_total(self):
        statement = self._statement.options(lazyload('*')).order_by(None).subquery('total')
        logger.debug(statement)
        return db.session.scalar(select(func.COUNT()).select_from(statement))

    @property
    def _limit(self) -> int | None:
        if self.per_page == 0:
            return None
        return self.per_page

    @property
    def _offset(self) -> int | None:
        if self.per_page:
            return (self.page - 1) * self.per_page
        return None

    @property
    def page(self) -> int:
        return self._page or 1

    @property
    def per_page(self) -> int:
        return self._per_page

    @property
    def pages(self) -> int:
        if self.per_page == 0:
            pages = 1
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1

    @property
    def previous(self) -> int:
        if not self.has_previous:
            return 0
        return self.page - 1

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def next(self) -> int:
        if not self.has_next:
            return 0
        return self.page + 1

    def __repr__(self):
        return f"Pagination(page={self.page}, per_page={self.per_page}, pages={self.pages}, total={self.total}, " \
               f"has_next={self.has_next}, next={self.next}, has_previous={self.has_previous}, previous={self.previous}, " \
               f"items={self.items})"