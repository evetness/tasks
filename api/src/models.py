from datetime import datetime, timedelta

from sqlmodel import Field
from api.src.core.models import Base


class Project(Base, table=True):
    name: str


class Task(Base, table=True):
    name: str | None
    start: datetime = Field(default_factory=datetime.now)
    end: datetime | None

    @property
    def elapsed(self) -> timedelta:
        if not self.end:
            return timedelta(days=0)
        return self.end - self.start
