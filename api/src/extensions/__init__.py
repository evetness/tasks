from alchemical.flask import Alchemical
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from sqlmodel import SQLModel

db = Alchemical(
    naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }, 
    model_class=SQLModel
)
migrate = Migrate(compare_type=True)
cache = Cache()
cors = CORS()
