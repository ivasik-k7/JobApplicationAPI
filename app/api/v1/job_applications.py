from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Body, Depends, Path
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from app.api.filtration import JobApplicationsFiltration
from app.api.pagination import OffsetPagination, PagePagination
from app.core.models.job_application import JobApplicationCreate, JobApplicationRead
from app.db.base import get_session
from app.db.models.job_application import JobApplication
from app.utils.tags import ApplicationTags

router = APIRouter(
    tags=[ApplicationTags.applications],
)


@router.get(
    "/",
    response_model=list[JobApplicationRead],
)
async def get_applications(
    pagination: Annotated[
        OffsetPagination,
        Depends(OffsetPagination),
    ],
    filtration: Annotated[
        JobApplicationsFiltration,
        Depends(JobApplicationsFiltration),
    ],
    session: Session = Depends(get_session),
):
    query = select(JobApplication).offset(pagination.offset).limit(pagination.limit)
    result = session.exec(query).all()

    applications = [
        jsonable_encoder(JobApplicationRead.model_validate(app)) for app in result
    ]

    return JSONResponse(status_code=200, content=applications)


@router.get(
    "/{id}",
    response_model=JobApplicationRead,
)
async def get_application(
    id: Annotated[str, Path(max_length=55)],
    session: Session = Depends(get_session),
):
    job_application = session.get(JobApplication, id)
    if not job_application:
        raise HTTPException(status_code=404, detail="Job application not found")

    return JSONResponse(
        status_code=204,
        content={},
    )


@router.post(
    "/",
    response_model=JobApplicationRead,
)
async def create_application(
    body: Annotated[JobApplicationCreate, Body()],
    session: Session = Depends(get_session),
):
    db_job_application = JobApplication.model_validate(body)

    session.add(db_job_application)
    session.commit()
    session.refresh(db_job_application)

    response_model = jsonable_encoder(
        JobApplicationRead.model_validate(db_job_application)
    )

    return JSONResponse(
        status_code=201,
        content=response_model,
    )


@router.put(
    "/{id}",
    response_model=JobApplicationRead,
)
async def update_application(
    id: Annotated[str, Path()],
    body: Annotated[JobApplicationCreate, Body()],
    session: Session = Depends(get_session),
):
    db_job_application = session.get(JobApplication, id)

    if not db_job_application:
        raise HTTPException(status_code=404, detail="Job application not found")

    job_application_data = body.model_dump(exclude_unset=True)

    for key, value in job_application_data.items():
        setattr(db_job_application, key, value)

    session.add(db_job_application)
    session.commit()
    session.refresh(db_job_application)

    obj = jsonable_encoder(JobApplicationRead.model_validate(db_job_application))

    return JSONResponse(
        status_code=200,
        content=obj,
    )


@router.delete(
    "/{id}",
    response_model=dict,
)
async def delete_application(
    id: Annotated[str, Path()],
    session: Session = Depends(get_session),
):
    job_application = session.get(JobApplication, id)
    if not job_application:
        raise HTTPException(status_code=404, detail="Job application not found")

    session.delete(job_application)
    session.commit()

    response = jsonable_encoder(JobApplicationRead.model_validate(job_application))

    return JSONResponse(
        status_code=200,
        content=response,
    )
