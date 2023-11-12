import datetime

from loguru import logger


def parse_date(value: str, raise_error: bool = False):
    formats = ["%Y", "%Y-%m", "%Y-%m-%d"]
    for frmt in formats:
        try:
            return datetime.datetime.strptime(value, frmt)
        except ValueError as e:
            logger.debug(f"Format error: {e}")
    if raise_error:
        raise ValueError(f"Not a valid date format: '{value}'")

    return None


def timedelta_to_string(time: datetime.timedelta) -> str:
    if time.total_seconds() <= 0:
        return "00:00"
    hours = (time.days * 24) + time.seconds // 3600
    minutes = (time.seconds // 60) % 60
    return f"{hours}:{minutes:0>2}"
