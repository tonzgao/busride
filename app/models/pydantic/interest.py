from typing import Optional
from pydantic import BaseModel

from .base import Base


class Interest(Base):
    entity_id: int
    user_id: int


class InterestCreateIn(BaseModel):
    entity_id: int
    data: Optional[dict] = None
