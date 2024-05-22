from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.job_applications import router as applications_router
from app.db.base import init_db
from app.utils.logger import LoggerFactory

factory = LoggerFactory()
logger = factory.create_logger(name="my_logger", filename="main.log")

logger.info("Application about to start!")


def create_app():
    app = FastAPI(
        title="Company records API",
        description="API designed to be as a source for tracking company applying records",
    )

    @app.on_event("startup")
    def on_startup():
        init_db()

    logger.info("Application has been instanced!")

    app.include_router(health_router)
    app.include_router(applications_router)

    logger.info("Routes as been registered!")

    return app


app = create_app()
