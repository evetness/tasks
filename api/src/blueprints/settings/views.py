from apiflask import APIBlueprint

from src.blueprints.settings.schemas import SettingBase, SettingQuery, SettingRead
from src.blueprints.settings.services import delete_setting, read_setting, save_setting


bp = APIBlueprint(
    "settings", __name__,
    url_prefix="/settings",
    tag={
        "name": "Settings"
    }
)


@bp.get("/<string:name>")
@bp.input(SettingQuery.Schema, location="query")
@bp.output(SettingRead.Schema)
def get_setting(name: str, query_data: SettingQuery):
    return read_setting(name=name, language=query_data.language)


@bp.put("/<string:name>")
@bp.input(SettingBase.Schema)
@bp.output(SettingRead.Schema)
def save_a_setting(name: str, json: SettingBase):
    return save_setting(name=name, language=json.language, content=json.content)


@bp.delete("/<string:name>")
@bp.input(SettingQuery.Schema, location="query")
@bp.output({})
def delete_a_setting(name: str, query: SettingQuery):
    delete_setting(name=name, language=query.language)
    return ""