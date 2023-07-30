from apiflask import HTTPError


class DatabaseInsertError(HTTPError):
    status_code = 500
    detail = {"error": "DATABASE_INSERT_ERROR"}


class DatabaseDeleteError(HTTPError):
    status_code = 500
    detail = {"error": "DATABASE_DELETE_ERROR"}
