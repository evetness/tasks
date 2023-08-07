from apiflask import HTTPError
from loguru import logger
from sqlmodel import select, text

from src.blueprints.wages.schemas import WageCreate, WageQuery, WageUpdate
from src.extensions import db
from src.extensions.alchemical.models import Pagination
from src.models import Wage


def read_wages(query: WageQuery) -> Pagination:
    logger.debug(query)

    where = []
    if query.project_id:
        where.append(Wage.project_id == query.project_id)
    
    statement = select(Wage) \
        .where(*where) \
        .order_by(text(f"{query.order_by} {query.order}"))
    logger.debug(statement)

    result = Pagination(page=query.page, per_page=query.per_page, statement=statement)
    logger.debug(result)

    return result


def create_wage(data: WageCreate) -> Wage:
    logger.debug(data)

    statement = select(Wage).where(Wage.date == data.date, Wage.project_id == data.project_id)
    logger.debug(statement)

    _wage = db.session.scalar(statement)
    if _wage:
        logger.warning(f"Wage Already Exists: {_wage.id} - {_wage.date} - {_wage.project_id}")
        raise HTTPError(409, "Wage Already Exists")
    
    result = Wage(
        date=data.date,
        amount=data.amount,
        currency=data.currency,
        project_id=data.project_id
    ).save()
    logger.debug(result)

    return result


def read_wage(ident: int) -> Wage:
    logger.debug(ident)

    result = db.session.get(Wage, ident)
    if not result:
        logger.warning(f"Wage Not Exists: {ident}")
        raise HTTPError(404, "Wage Not Exists")
    logger.debug(result)

    return result


def update_wage(ident: int, data: WageUpdate) -> Wage:
    logger.debug(ident)
    logger.debug(data)

    result = read_wage(ident)

    statement = select(Wage).where(Wage.id != ident, Wage.date == data.date, Wage.project_id == result.project_id)
    logger.debug(statement)

    _wage = db.session.scalar(statement)
    if _wage:
        logger.warning(f"Wage Already Exists: {_wage.id} - {_wage.date}")
        raise HTTPError(409, "Wage Already Exists")

    result.update(
        date=data.date,
        amount=data.amount,
        currency=data.currency
    ).save()
    logger.debug(result)

    return result


def delete_wage(ident: int) -> None:
    logger.debug(ident)

    result = read_wage(ident)
    result.delete()
