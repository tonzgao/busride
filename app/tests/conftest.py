import pytest
from starlette.config import environ

from ..settings.globals import DATABASE_CONFIG
from ..application import db

environ["TESTING"] = "True"


@pytest.fixture(autouse=True)
async def bind():
    await db.set_bind(DATABASE_CONFIG.db)
