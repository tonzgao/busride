from pydantic import BaseModel

from .base import Base


class Entity(Base):
    identifier: str
    data: dict


class EntityCreateIn(BaseModel):
    identifier: str