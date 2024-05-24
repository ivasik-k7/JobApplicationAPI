from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class JobApplicationStatus(str, Enum):
    REVIEWING = "reviewing"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"


class JobApplication(SQLModel, table=True):
    __tablename__: str = "job_applications"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    company: str = Field(default="Unknown")
    status: JobApplicationStatus = Field(default=JobApplicationStatus.REVIEWING)
    url: str | None = Field(max_length=255)

    applied_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)

    user_id: UUID | None = Field(default=None, foreign_key="users.id")

    user: "User" = Relationship(back_populates="job_applications")


from app.db.models.user import User  # noqa
