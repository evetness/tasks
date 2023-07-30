from apiflask import APIBlueprint

from src.blueprints.wages.schemas import WageCreate, WagePagination, WageQuery, WageRead, WageUpdate
from src.blueprints.wages.services import create_wage, delete_wage, read_wage, read_wages, update_wage


bp = APIBlueprint(
    "wages", __name__,
    url_prefix="/wages",
    tag={
        "name": "Wages"
    }
)


@bp.get("")
@bp.input(WageQuery.Schema, location="query")
@bp.output(WagePagination.Schema)
def get_wages(query: WageQuery):
    return read_wages(query=query)


@bp.post("")
@bp.input(WageCreate.Schema)
@bp.output(WageRead.Schema)
def add_a_wage(json: WageCreate):
    return create_wage(data=json)


@bp.get("/<int:id>")
@bp.output(WageRead.Schema)
def get_a_wage(id: int):
    return read_wage(ident=id)


@bp.put("/<int:id>")
@bp.input(WageUpdate.Schema)
@bp.output(WageRead.Schema)
def modify_a_wage(id: int, json: WageUpdate):
    return update_wage(ident=id, data=json)


@bp.delete("/<int:id>")
@bp.output({})
def remove_a_wage(id: int):
    delete_wage(ident=id)
    return {}
