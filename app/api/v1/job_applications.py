from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.params import Body, Depends, Path
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from app.api.filtration import JobApplicationsFiltration
from app.api.pagination import OffsetPagination
from app.core.models.job_application import JobApplicationCreate, JobApplicationRead
from app.core.security import oauth2_scheme
from app.db.base import get_session
from app.db.models.job_application import JobApplication
from app.db.models.user import User
from app.utils.tags import ApplicationTags
from app.utils.token import decode_access_token

router = APIRouter(
    tags=[ApplicationTags.applications],
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    token_data = decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = token_data.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    query = select(User).filter(User.username == username)
    user = session.exec(query).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


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
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    query = (
        select(JobApplication)
        .where(JobApplication.user_id == str(user.id))
        .offset(pagination.offset)
        .limit(pagination.limit)
    )

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
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    job_query = (
        select(JobApplication)
        .where(JobApplication.id == id)
        .where(JobApplication.user_id == str(user.id))
    )
    job_application = session.exec(job_query).first()
    if not job_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    obj = jsonable_encoder(JobApplicationRead.model_validate(job_application))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=obj,
    )


@router.post(
    "/",
    response_model=JobApplicationRead,
)
async def create_application(
    body: Annotated[JobApplicationCreate, Body()],
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_job_application = JobApplication.model_validate(body)
    db_job_application.user = user

    session.add(db_job_application)
    session.commit()
    session.refresh(db_job_application)

    response_model = jsonable_encoder(
        JobApplicationRead.model_validate(db_job_application)
    )

    return JSONResponse(status_code=201, content=response_model)


@router.put(
    "/{id}",
    response_model=JobApplicationRead,
)
async def update_application(
    id: Annotated[str, Path()],
    body: Annotated[JobApplicationCreate, Body()],
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    query = select(JobApplication).where(JobApplication.id == id)
    db_job_application = session.exec(query)

    if not db_job_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    if db_job_application.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    job_application_data = body.model_dump(exclude_unset=True)

    for key, value in job_application_data.items():
        setattr(db_job_application, key, value)

    session.add(db_job_application)
    session.commit()
    session.refresh(db_job_application)

    obj = jsonable_encoder(JobApplicationRead.model_validate(db_job_application))

    return JSONResponse(status_code=status.HTTP_200_OK, content=obj)


@router.delete(
    "/{id}",
    response_model=dict,
)
async def delete_application(
    id: Annotated[str, Path()],
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    query = select(JobApplication).where(JobApplication.id == id)
    job_application = session.exec(query).first()
    if not job_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    if job_application.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    session.delete(job_application)
    session.commit()

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={},
    )
