from typing import Any, Optional, Union

from pydantic import BaseModel, PostgresDsn, validator
from pydantic.fields import Field
from sqlalchemy.engine.url import URL
from starlette.datastructures import Secret


class DatabaseURL(BaseModel):
    db: PostgresDsn

    @validator("db")
    def check_db_name(cls, v):
        assert v.path and len(v.path) > 1, "database must be provided"
        return v
