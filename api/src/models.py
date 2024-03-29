import datetime
from typing import List, Optional
from sqlalchemy import Column

from sqlmodel import Field, Relationship
from src.constants import HOUR
from src.extensions.alchemical.models import Base

from src.utils import timedelta_to_string


class Wage(Base, table=True):
    date: datetime.date = Field(default_factory=datetime.date.today)
    amount: int
    currency: str = Field(max_length=3)
    
    project_id: int = Field(foreign_key="project.id")
    project: "Project" = Relationship(back_populates="wages")


class Project(Base, table=True):
    name: str = Field(max_length=255)

    wages: List["Wage"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    tasks: List["Task"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Task(Base, table=True):
    name: Optional[str] = Field(max_length=255)
    start: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end: Optional[datetime.datetime]
    completed: bool = Field(default=False)

    project_id: int = Field(foreign_key="project.id")
    project: "Project" = Relationship(back_populates="tasks")

    wage: Optional["Wage"] = Relationship(
        sa_relationship_kwargs=dict(
            primaryjoin="(foreign(Wage.date) <= Task.start) & (foreign(Wage.project_id) == Task.project_id)",
            lazy="joined",
            uselist=False,
            viewonly=True
        )
    )

    @property
    def elapsed(self) -> str:
        if not self.end:
            return "00:00"
        result = self.end - self.start
        return timedelta_to_string(result)
    
    @property
    def amount(self) -> float:
        if not self.wage:
            return 0.0

        hours, minutes = self.elapsed.split(":")
        elapsed = datetime.timedelta(
            hours=int(hours),
            minutes=int(minutes),
            seconds=0)
        return round((elapsed.total_seconds() / HOUR) * self.wage.amount, 2)
    
    @property
    def currency(self) -> str | None:
        if not self.wage:
            return None
        return self.wage.currency


class Setting(Base, table=True):
    name: str = Field(max_length=255)
    content: Optional[str] = Field(default=None, max_length=255)
    language: Optional[str] = Field(default=None, max_length=255)