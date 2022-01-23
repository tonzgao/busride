from enum import Enum

from pydantic import BaseModel

from .base import Base


class ApiEnum(str, Enum):
    tmdb = "tmdb"


class Api(Base):
    name: ApiEnum
    data: dict
    is_active: bool = True


class ApiCreateIn(BaseModel):
    name: ApiEnum
    data: dict
