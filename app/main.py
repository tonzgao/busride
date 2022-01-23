# isort:skip_file

import sys

sys.path.extend(["./"])

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.datastructures import Secret

from app.application import app
from app.routes.users import router as user_router
from app.routes.entities import router as entity_router
from app.routes.apis import router as api_router
from app.routes.interests import router as interest_router
from app.routes.auth import router as auth_router
from app.routes.rss import router as rss_router
from app.settings.globals import SENTRY_DSN


ROUTERS = (
    user_router,
    entity_router,
    api_router,
    interest_router,
    auth_router,
    rss_router,
)

for r in ROUTERS:
    app.include_router(r)

if isinstance(SENTRY_DSN, Secret) and SENTRY_DSN.__str__() not in ("None", ""):
    app.add_middleware(SentryAsgiMiddleware)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info")
