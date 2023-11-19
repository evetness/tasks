import os
import sys
from apiflask import APIFlask
from loguru import logger
from werkzeug.middleware.proxy_fix import ProxyFix

from src.extensions import db, migrate, cors, cache
from config import Config

__version__ = "0.1.0"


def create_app(environment: str | None = None):
    app = APIFlask(
        __name__,
        docs_ui="redoc",
        docs_path="/"
    )
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    register_configs(app, environment)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_context(app)

    return app


def register_configs(app: APIFlask, environment: str | None):
    config = Config(_env_file=".env.testing") if environment == "testing" else Config()

    app.title = config.TITLE
    app.version = __version__
    app.config.from_prefixed_env()
    app.config.from_mapping(config.dict())

    if not config.TESTING:
        register_logger(config)


def register_logger(config: Config):
    logger.remove()

    os.makedirs(config.LOGS_DIRECTORY, exist_ok=True)
    file = os.path.join(config.LOGS_DIRECTORY, "oas.log")

    level = config.LOG_LEVEL
    if config.DEBUG:
        level = "DEBUG"

    logger.add(file, rotation="00:00", retention="1 week", level=level, delay=True)
    logger.add(sys.stdout, level=level)


def register_blueprints(app: APIFlask):
    from src.blueprints.projects.views import bp as projects
    from src.blueprints.tasks.views import bp as tasks
    from src.blueprints.settings.views import bp as settings

    app.register_blueprint(projects)
    app.register_blueprint(tasks)
    app.register_blueprint(settings)


def register_commands(app: APIFlask):
    ...


def register_extensions(app: APIFlask):
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    cors.init_app(app)


def register_context(app: APIFlask):
    from src.models import Project, Wage, Task
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            db=db,
            cache=cache,
            Project=Project,
            Wage=Wage,
            Task=Task
        )

    @app.error_processor
    def error_processor(e):
        if e.status_code == 422:
            logger.error(f"Validation Error - {e.detail}")
        return {"message": e.message, "detail": e.detail, **e.extra_data}, e.status_code, e.headers
