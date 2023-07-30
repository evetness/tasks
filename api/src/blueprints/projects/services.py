from loguru import logger
from sqlmodel import col, select, text
from src.blueprints.projects.schemas import ProjectQuery, ProjectWrite, Unpaid
from src.extensions import db
from src.extensions.alchemical.models import Pagination
from src.models import Project, Task, Wage


def create_project(data: ProjectWrite) -> Project:
    logger.debug(data)

    statement = select(Project).where(Project.name == data.name)
    logger.debug(statement)

    _project = db.session.scalar(statement)
    if _project:
        logger.warning(f"Project Already Exists: {_project.id} - {_project.name}")

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


def read_project(ident: int) -> Project:
    logger.debug(ident)

    result = db.session.get(Project, ident)
    if not result:
        logger.warning(f"Project Not Exists: {ident}")
    logger.debug(result)

    return result


def update_project(ident: int, data: ProjectWrite) -> Project:
    logger.debug(ident)
    logger.debug(data)

    statement = select(Project).where(Project.id != ident, Project.name == data.name)
    logger.debug(statement)

    _project = db.session.scalar(statement)
    if _project:
        logger.warning(f"Project Already Exists: {_project.id} - {_project.name}")
    
    result = read_project(ident)
    result.update(name=data.name).save()
    logger.debug(result)

    return result


def delete_project(ident: int) -> None:
    logger.debug(ident)

    result = read_project(ident)
    result.delete()


def project_current_salary(ident: int) -> Wage | None:
    logger.debug(ident)

    project = read_project(ident)

    statement = select(Wage) \
        .where(Wage.project_id == project.id) \
        .order_by(Wage.date.desc())
    logger.debug(statement)

    result = db.session.scalar(statement)
    logger.debug(result)

    return result


def calculate_unpaid_wage(ident: int) -> Unpaid | None:
    logger.debug(ident)

    project = read_project(ident)

    statement = select(Task) \
        .where(Task.project_id == project.id)
    logger.debug(statement)

    result = db.session.scalars(statement).all()
    logger.debug(result)

    if not result:
        return None
    
    current_salary = project_current_salary(project.id)

    return Unpaid(
        amount=round(sum(task.amount for task in result), 2),
        currency=current_salary.currency if current_salary else None
    )


    