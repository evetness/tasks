from dataclasses import dataclass, field
import datetime
from typing import List
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
        # Validate the end date to be later then the start date
        if data["end"] is not None and data["end"] <= data["start"]:
            raise ValidationError("The end date must be later then the start date")


@dataclass
@add_schema
class TaskRead(TaskBase):
    id: int
    elapsed: Time
    amount: float
    currency: str
    completed: bool


@dataclass
@add_schema
class TaskCreate(TaskBase):
    project_id: int


@dataclass
@add_schema
class TaskUpdate(TaskBase):
    ...


class TaskOrderBy(OrderBy):
    name = "name"
    start = "start"
    end = "end"


@dataclass
@add_schema
class TaskQuery(Query):
    order_by: TaskOrderBy = field(default=TaskOrderBy.name)
    search: str | None = None
    project_id: int = field(default=0, metadata={"required": True})


@dataclass
@add_schema
class TaskPagination(Pagination):
    items: List[TaskRead]

