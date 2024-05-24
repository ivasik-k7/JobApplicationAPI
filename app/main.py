from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.job_applications import router as applications_router
from app.db.base import init_db
from app.utils.logger import LoggerFactory

factory = LoggerFactory()
logger = factory.create_logger(name="my_logger", filename="main.log")


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    init_db()
    yield
    print("clean up lifespan")


def create_app():
    logger.info("Application about to start!")

    app = FastAPI(
        title="Company records API",
        description="API designed to be as a source for tracking company applying records",
        lifespan=app_lifespan,
    )

    logger.info("Application has been instanced!")

    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(applications_router, prefix="/api/v1")

    logger.info("Routes as been registered!")

    return app


app = create_app()
