import datetime

from apiflask import HTTPError
from loguru import logger
from sqlmodel import col, select, text
from src.blueprints.projects.schemas import ProjectQuery, ProjectWrite, Salary, WageWrite
from src.extensions import db
from src.extensions.alchemical.models import Pagination
from src.models import Project, Task, Wage

from src.utils import timedelta_to_string


def create_project(data: ProjectWrite) -> Project:
    logger.debug(data)

    statement = select(Project).where(Project.name == data.name)
    logger.debug(statement)

    _project = db.session.scalar(statement)
    if _project:
        logger.warning(f"Project Already Exists: {_project.id} - {_project.name}")
        raise HTTPError(status_code=409, message="Project Already Exists")

    result = Project(name=data.name).save()
    logger.debug(result)
    
    return result


def read_projects(query: ProjectQuery) -> Pagination:
    logger.debug(query)

    where = []
    if query.search:
        where.append(col(Project.name).contains(query.search))
    
    statement = select(Project) \
        .where(*where) \
        .order_by(text(f"{query.order_by} {query.order}"))
    logger.debug(statement)

    result = Pagination(page=query.page, per_page=query.per_page, statement=statement)
    logger.debug(result)

    return result


def read_project(project_id: int) -> Project:
    logger.debug(project_id)

    result = db.session.get(Project, project_id)
    if not result:
        logger.warning(f"Project Not Exists: {project_id}")
        raise HTTPError(status_code=404, message="Project Not Exists")
    logger.debug(result)

    return result


def update_project(project_id: int, data: ProjectWrite) -> Project:
    logger.debug(project_id)
    logger.debug(data)

    statement = select(Project).where(Project.id != project_id, Project.name == data.name)
    logger.debug(statement)

    _project = db.session.scalar(statement)
    if _project:
        logger.warning(f"Project Already Exists: {_project.id} - {_project.name}")
        raise HTTPError(status_code=409, message="Project Already Exists")
    
    result = read_project(project_id)
    result.update(name=data.name).save()
    logger.debug(result)

    return result


def delete_project(project_id: int) -> None:
    logger.debug(project_id)

    result = read_project(project_id)
    result.delete()


def read_current_wage(project_id: int) -> Wage | None:
    logger.debug(project_id)

    statement = select(Wage) \
        .where(Wage.project_id == project_id) \
        .order_by(Wage.date.desc())
    logger.debug(statement)

    result = db.session.scalar(statement)
    if not result:
        logger.warning(f"Wage Not Exists: {project_id}")
        return None
    logger.debug(result)

    return result


def save_wage(project_id: int, data: WageWrite) -> Wage:
    logger.debug(project_id)
    logger.debug(data)

    statement = select(Wage).where(Wage.date == data.date, Wage.project_id == project_id)
    logger.debug(statement)

    result = db.session.scalar(statement)
    if result:
        result.update(amount=data.amount, currency=data.currency)
    else:
        result = Wage(date=data.date, amount=data.amount, currency=data.currency, project_id=project_id)

    result.save()
    logger.debug(result)
    
    return result
   

def delete_wage(project_id: int) -> Wage | None:
    logger.debug(project_id)

    statement = select(Wage) \
        .where(Wage.project_id == project_id) \
        .order_by(Wage.date.desc())
    logger.debug(statement)

    result = db.session.scalar(statement)
    if not result:
        logger.warning(f"Wage Not Exists: {project_id}")
        raise HTTPError(status_code=409, message="Wage Not Exists")

    logger.debug(result)
    result.delete()

    return result


def read_salary(project_id: int) -> Salary | None:
    logger.debug(project_id)

    statement = select(Task) \
        .where(Task.project_id == project_id, Task.completed == 0)
    logger.debug(statement)

    result = db.session.scalars(statement).unique().all()
    logger.debug(result)

    if not result:
        logger.warning(f"Tasks Not Exists: {project_id}")
        return Salary(
            amount=0,
            elapsed="00:00",
            currency=""
        )
    
    task: Task = next(iter(result))

    amount = round(sum(task.amount for task in result), 2)
    elapsed = datetime.timedelta(hours=0, minutes=0)
    for task in result:
        hours, minutes = task.elapsed.split(":")
        elapsed += datetime.timedelta(hours=int(hours), minutes=int(minutes))

    return Salary(
        amount=amount,
        elapsed=timedelta_to_string(elapsed),
        currency=task.currency
    )


    