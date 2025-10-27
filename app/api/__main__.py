import logging
import time
from functools import partial

import uvicorn
from dishka import AsyncContainer, make_async_container
from dishka.integrations import fastapi as DishkaIntegration
from fastapi import FastAPI

from app.api.v1 import v1_router
from app.config import settings
from app.migrations import apply_migrations
from app.repository.provider import RepositoryProvider

logger = logging.getLogger(__name__)


async def on_startup():
    apply_migrations(database_dsn=settings.database_dsn, migrations_path=settings.migrations_path)
    logger.info("Application startup success!")


async def on_shutdown(container: AsyncContainer):
    await container.close()
    logger.info("Application shutdown success!")


def create_app() -> FastAPI:
    time_start = time.monotonic()
    logger.info("Creating application..")
    if settings.enable_docs:
        app = FastAPI(title="aiti_guru-test_task")
    else:
        app = FastAPI(title="aiti_guru-test_task", openapi_url="", docs_url="", redoc_url="")
    logger.info("Creating DI container..")
    container = make_async_container(DishkaIntegration.FastapiProvider(), RepositoryProvider())
    DishkaIntegration.setup_dishka(container=container, app=app)
    startup = partial(on_startup)
    app.include_router(v1_router)
    app.add_event_handler("startup", startup)
    shutdown = partial(on_shutdown, container)
    app.add_event_handler("shutdown", shutdown)
    time_elapsed = time.monotonic() - time_start
    logger.info("Creating application success! (time=%s)", time_elapsed)
    return app


if __name__ == "__main__":
    uvicorn.run(
        app="app.api.__main__:create_app",
        host="0.0.0.0",
        port=settings.backend_port,
        reload=settings.auto_reload,
        factory=True,
        access_log=False,
        log_level=settings.log_level,
    )
