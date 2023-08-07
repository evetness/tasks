import datetime
from typing import List, Optional
from loguru import logger

from sqlmodel import Field, Relationship, select, col
from src.constants import HOUR
from src.extensions import db, cache
from src.extensions.alchemical.models import Base


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

    @property
    def elapsed(self) -> datetime.time:
        if not self.end:
            return 0
        result = self.end - self.start
        result = datetime.datetime.strptime(str(result), "%H:%M:%S")
        return result.time()
    
    @property
    def amount(self) -> float:
        wage = self.current_salary()
        if not wage:
            return 0.0
        
        elapsed = datetime.timedelta(
            hours=self.elapsed.hour, 
            minutes=self.elapsed.minute, 
            seconds=self.elapsed.second)
        return round((elapsed.seconds / HOUR) * wage.amount, 2)
    
    @property
    def currency(self) -> str | None:
        wage = self.current_salary()
        if not wage:
            return None
        return wage.currency

    @cache.memoize(5)
    def current_salary(self) -> Wage | None:
        statement = select(Wage) \
            .where(
                Wage.date <= self.start.date(), 
                Wage.project_id == self.project_id) \
            .order_by(col(Wage.date).desc())
        logger.debug(statement)

        result = db.session.scalar(statement)
        logger.debug(result)

        return result
