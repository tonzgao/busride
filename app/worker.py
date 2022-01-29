# isort:skip_file

import sys

sys.path.extend(["./"])

from pydantic.utils import import_string

from .application import db
from .settings.arq import settings
from .settings.globals import (
    ARQ_BACKGROUND_FUNCTIONS,
    ARQ_CRONJOBS,
    DATABASE_CONFIG,
)

print("here", ARQ_BACKGROUND_FUNCTIONS, ARQ_CRONJOBS)

FUNCTIONS: list = [
    import_string(background_function)
    for background_function in list(ARQ_BACKGROUND_FUNCTIONS)
] if ARQ_BACKGROUND_FUNCTIONS is not None else list()

CRONJOBS: list = [
    import_string(cronjob) for cronjob in list(ARQ_CRONJOBS)
] if ARQ_CRONJOBS is not None else list()
print("wtf", CRONJOBS)


async def startup(ctx):
    """
    Binds a connection set to the db object.
    """
    await db.set_bind(DATABASE_CONFIG.db)


async def shutdown(ctx):
    """
    Pops the bind on the db object.
    """
    await db.pop_bind().close()


class WorkerSettings:
    """
    Settings for the ARQ worker.
    """

    on_startup = startup
    on_shutdown = shutdown
    redis_settings = settings
    functions: list = FUNCTIONS
    cron_jobs: list = CRONJOBS
