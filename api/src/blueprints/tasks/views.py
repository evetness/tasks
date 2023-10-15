from apiflask import APIBlueprint

from src.blueprints.tasks.schemas import TaskPagination, TaskQuery, TaskRead, TaskCreate, TaskUpdate, TaskComplete
from src.blueprints.tasks.services import create_task, delete_task, read_task, read_tasks, update_task, \
    update_tasks_status

bp = APIBlueprint(
    "tasks", __name__,
    url_prefix="/tasks",
    tag={
        "name": "Tasks"
    }
)


@bp.get("")
@bp.input(TaskQuery.Schema, location="query")
@bp.output(TaskPagination.Schema)
def get_tasks(query: TaskQuery):
    return read_tasks(query=query)


@bp.post("")
@bp.input(TaskCreate.Schema)
@bp.output(TaskRead.Schema)
def add_a_task(json: TaskCreate):
    return create_task(data=json)


@bp.get("/<int:id>")
@bp.output(TaskRead.Schema)
def get_a_task(id: int):
    return read_task(ident=id)


@bp.put("/<int:id>")
@bp.input(TaskUpdate.Schema)
@bp.output(TaskRead.Schema)
def modify_a_task(id: int, json: TaskUpdate):
    return update_task(ident=id, data=json)


@bp.put("/complete")
@bp.input(TaskComplete.Schema)
@bp.output(TaskRead.Schema(many=True))
def complete_tasks(json: TaskComplete):
    return update_tasks_status(data=json)


@bp.delete("/<int:id>")
@bp.output({})
def remove_a_task(id: int):
    delete_task(ident=id)
    return {}
