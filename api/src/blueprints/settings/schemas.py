from dataclasses import dataclass, field
from marshmallow import post_load

from marshmallow_dataclass import add_schema

from src.extensions.marshmallow_dataclass.schemas import Base


@dataclass
@add_schema
class SettingBase(Base):
    content: str = field(metadata={"type": "string <longtext>"})
    language: str | None

  
@dataclass
@add_schema
class SettingRead(SettingBase):
    name: str
  

@dataclass
@add_schema
class SettingQuery(Base):
    language: str | None

    @post_load
    def load_language(self, data, **kwargs):
        if data["language"] == "":
            data["language"] = None
        return data
