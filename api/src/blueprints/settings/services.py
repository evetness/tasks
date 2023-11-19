from loguru import logger
from werkzeug.exceptions import NotFound

from src.extensions import db
from src.models import Setting


def read_setting(name: str, language: str | None = None) -> Setting | None:
    logger.debug(name)
    logger.debug(language)

    statement = Setting.select().where(Setting.name == name, Setting.language == language)
    logger.debug(statement)

    result = db.session.scalar(statement)
    if not result:
        logger.warning(f"Settings Not Found: {name} {language}")
        raise NotFound
    logger.debug(result)

    return result


def save_setting(name: str, language: str | None, content: str) -> Setting:
    logger.debug(name)
    logger.debug(language)
    logger.debug(content)

    statement = Setting.select().where(Setting.name == name, Setting.language == language)
    logger.debug(statement)

    result = db.session.scalar(statement)
    if result:
        logger.debug("Setting Exists - Updating")
        result = result.update(content=content).save()
    else:
        logger.debug("Setting Not Exists - Creating")
        result = Setting(name=name, language=language, content=content).save()
    logger.debug(result)

    return result


def delete_setting(name: str, language: str | None) -> None:
    logger.debug(name)
    setting = read_setting(name, language)
    setting.delete()
