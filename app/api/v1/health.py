from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response

from app.utils.tags import ApplicationTags

router = APIRouter(tags=[ApplicationTags.health])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy"},
    )


@router.get("/health/details", status_code=status.HTTP_200_OK)
async def detailed_health_check() -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "database_status": "TODO",
            "service_a_status": "TODO",
            "service_b_status": "TODO",
        },
    )
