from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from sqlmodel import SQLModel

from app.db.models.job_application import JobApplicationStatus


class JobApplicationCreate(BaseModel):
    company: str
    status: JobApplicationStatus
    url: str | None


class JobApplicationRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company: str
    status: JobApplicationStatus
    url: str | None
    applied_at: datetime
    updated_at: datetime | None
