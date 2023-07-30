from apiflask import APIBlueprint

from src.blueprints.projects.schemas import ProjectPagination, ProjectQuery, ProjectRead, ProjectWrite, Unpaid
from src.blueprints.projects.services import create_project, delete_project, read_project, read_projects, update_project, calculate_unpaid_wage, project_current_salary
from src.blueprints.wages.schemas import WageRead


bp = APIBlueprint(
    "projects", __name__,
    url_prefix="/projects",
    tag={
        "name": "Projects"
    }
)


@bp.get("")
@bp.input(ProjectQuery.Schema, location="query")
@bp.output(ProjectPagination.Schema)
def get_projects(query: ProjectQuery):
    return read_projects(query=query)


@bp.post("")
@bp.input(ProjectWrite.Schema)
@bp.output(ProjectRead.Schema)
def add_a_project(json: ProjectWrite):
    return create_project(data=json)


@bp.get("/<int:id>")
@bp.output(ProjectRead.Schema)
def get_a_project(id: int):
    return read_project(ident=id)


@bp.put("/<int:id>")
@bp.input(ProjectWrite.Schema)
@bp.output(ProjectRead.Schema)
def modify_a_project(id: int, json: ProjectWrite):
    return update_project(ident=id, data=json)


@bp.delete("/<int:id>")
@bp.output({})
def remove_a_project(id: int):
    delete_project(ident=id)
    return {}


@bp.get("/<int:id>/current-salary")
@bp.output(WageRead.Schema)
def get_current_salary(id: int):
    return project_current_salary(ident=id)


@bp.get("/<int:id>/unpaid-tasks")
@bp.output(Unpaid.Schema)
def calculate_unpaid_tasks(id: int):
    return calculate_unpaid_wage(ident=id)
