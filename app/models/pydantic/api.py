from pydantic import BaseModel

from .base import Base


class Api(Base):
    name: str
    data: dict
    is_active: bool = True


class ApiCreateIn(BaseModel):
    name: str
    data: dict
