from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

database_url = settings.DATABASE_URL

engine = create_engine(database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
