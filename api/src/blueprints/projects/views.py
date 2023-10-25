from apiflask import APIBlueprint

from src.blueprints.projects.schemas import ProjectPagination, ProjectQuery, ProjectRead, ProjectWrite, Salary, WageRead, WageWrite
from src.blueprints.projects.services import create_project, delete_project, delete_wage, read_project, read_projects, save_wage, update_project, read_current_wage, read_salary


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
    return read_project(project_id=id)


@bp.put("/<int:id>")
@bp.input(ProjectWrite.Schema)
@bp.output(ProjectRead.Schema)
def modify_a_project(id: int, json: ProjectWrite):
    return update_project(project_id=id, data=json)


@bp.delete("/<int:id>")
@bp.output({})
def remove_a_project(id: int):
    delete_project(project_id=id)
    return {}


@bp.get("/<int:id>/wage")
@bp.output(WageRead.Schema)
def get_current_wage(id: int):
    return read_current_wage(project_id=id)


@bp.put("/<int:id>/wage")
@bp.input(WageWrite.Schema)
@bp.output(WageRead.Schema)
def add_or_update_wage(id: int, json: WageWrite):
    return save_wage(project_id=id, data=json)


@bp.delete("/<int:id>/wage")
@bp.output({})
def remove_current_wage(id: int):
    return delete_wage(project_id=id)


@bp.get("/<int:id>/salary")
@bp.output(Salary.Schema)
def calculate_salary(id: int):
    return read_salary(project_id=id)
