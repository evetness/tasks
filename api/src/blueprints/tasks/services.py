import datetime
from typing import List
from apiflask import HTTPError

from loguru import logger
from sqlalchemy import or_
from sqlmodel import col, select, text
from src.blueprints.tasks.schemas import TaskCreate, TaskQuery, TaskUpdate, TaskComplete
from src.extensions import db
from src.extensions.alchemical.models import Pagination
from src.models import Task
from src.utils import parse_date


def create_task(data: TaskCreate) -> Task:
    logger.debug(data)

    # TODO check if start value is not in an already existing range
    statement = select(Task).where(Task.start <= data.start, Task.end >= data.start)
    logger.debug(statement)

    _task = db.session.scalar(statement)
    if _task:
        logger.warning(f"Task Already Exists: {_task.id} - {_task.start} - {_task.end}")
        raise HTTPError(409)
    
    result = Task(
        name=data.name,
        start=data.start,
        end=data.end,
        project_id=data.project_id
    ).save()
    logger.debug(result)

    return result


def read_tasks(query: TaskQuery) -> Pagination:
    logger.debug(query)

    where = []
    if query.project_id:
        where.append(Task.project_id == query.project_id)
    if query.status:
        status_query = {
            'COMPLETED': Task.completed == True,
            'INCOMPLETE': Task.completed == False
        }
        where.append(status_query[query.status])
    if query.search:
        search = [col(Task.name).contains(query.search)]

        dates = query.search.split("..")
        start = parse_date(dates[0])
        end = parse_date(dates[1]) if len(dates) > 1 else None

        if start and not end:
            search.append((Task.start >= start))
        elif start and end:
            search.append((Task.start >= start) & (Task.end <= end))
        
        where.append(or_(*search))

    statement = select(Task) \
        .where(*where) \
        .order_by(text(f"{query.order_by} {query.order}"))
    logger.debug(statement)

    result = Pagination(page=query.page, per_page=query.per_page, statement=statement)
    logger.debug(result)
    
    return result


def read_task(ident: int) -> Task:
    logger.debug(ident)

    result = db.session.get(Task, ident)
    if not result:
        logger.warning(f"Task Not Exists: {ident}")
        raise HTTPError(404)
    logger.debug(result)

    return result


def update_task(ident: int, data: TaskUpdate):
    logger.debug(ident)
    logger.debug(data)

    statement = select(Task).where(Task.id != ident, Task.start <= data.start, Task.end >= data.start)
    logger.debug(statement)

    _task = db.session.scalar(statement)
    if _task:
        logger.warning(f"Task Already Exists: {_task.id} - {_task.start} - {_task.end}")
        raise HTTPError(409)
    
    result = read_task(ident)
    result.update(
        name=data.name,
        start=data.start,
        end=data.end
    ).save()
    logger.debug(result)

    return result


def update_tasks_status(data: TaskComplete) -> List[Task]:
    logger.debug(data)

    statement = select(Task).where(Task.project_id == data.project_id, Task.end <= data.date)
    logger.debug(statement)

    result = db.session.scalars(statement)
    logger.debug(result)
    for task in result:
        task.update(completed=True)
        db.session.add(task)
    db.session.commit()

    return result


def change_task_status(ident: int) -> Task:
    logger.debug(ident)

    result = read_task(ident)
    result.update(completed=not result.completed).save()
    logger.debug(result)

    return result


def stop_task(ident: int) -> Task:
    logger.debug(ident)

    result = read_task(ident)
    if result.end:
        logger.warning(f"Task already done - {ident}")
        raise HTTPError(409)
    result.update(end=datetime.datetime.now()).save()
    logger.debug(result)

    return result


def delete_task(ident: int) -> None:
    logger.debug(ident)

    result = read_task(ident)
    result.delete()
    