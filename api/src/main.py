from apiflask import APIFlask
from werkzeug.middleware.proxy_fix import ProxyFix

from src.extensions import db, migrate, cors, cache
from config import Config


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
    app.version = config.VERSION
    app.config.from_object(config)


def register_blueprints(app: APIFlask):
    ...


def register_commands(app: APIFlask):
    ...


def register_extensions(app: APIFlask):
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    cors.init_app(app)


def register_context(app: APIFlask):
    @app.shell_context_processor
    def make_shell_context():
        return dict()
