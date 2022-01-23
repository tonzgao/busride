import pytest_asyncio
from starlette.config import environ

from ..application import db
from ..settings.globals import DATABASE_CONFIG

environ["TESTING"] = "True"


@pytest_asyncio.fixture(autouse=True)
async def bind():
    await db.set_bind(DATABASE_CONFIG.db)
