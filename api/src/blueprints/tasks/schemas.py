from dataclasses import dataclass, field
import datetime
from typing import List, Literal
from marshmallow import ValidationError, validates_schema, fields

from marshmallow_dataclass import NewType, add_schema

from src.extensions.marshmallow_dataclass.schemas import Base, OrderBy, Query, Pagination

Time = NewType("Time", str, field=fields.Time)


@dataclass
@add_schema
class TaskBase(Base):
    name: str | None
    start: datetime.datetime
    end: datetime.datetime | None

    @validates_schema
    def validate_task(self, data, **kwargs):
        # Validate the end date to be later than the start date
        if data["end"] is not None and data["end"] <= data["start"]:
            raise ValidationError("The end date must be later then the start date")


@dataclass
@add_schema
class TaskRead(TaskBase):
    id: int
    completed: bool
    elapsed: str
    amount: float
    currency: str


@dataclass
@add_schema
class TaskCreate(TaskBase):
    project_id: int


@dataclass
@add_schema
class TaskUpdate(TaskBase):
    ...


@dataclass
@add_schema
class TaskComplete(Base):
    project_id: int
    date: datetime.date


class TaskOrderBy(OrderBy):
    name = "name"
    start = "start"
    end = "end"


@dataclass
@add_schema
class TaskQuery(Query):
    order_by: TaskOrderBy = field(default=TaskOrderBy.name)
    search: str | None = None
    status: Literal['COMPLETED', 'INCOMPLETE'] | None = None
    project_id: int = field(default=0, metadata={"required": True})


@dataclass
@add_schema
class TaskPagination(Pagination):
    items: List[TaskRead]

