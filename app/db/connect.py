import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)


class PostgresConnectionManager:
    def __init__(
        self,
        connection_params=settings.DATABASE_URL,
    ):
        self.connection_params = connection_params
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(**self.connection_params)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.commit()
            self.connection.close()


class SessionManager:
    def __init__(self, engine=engine):
        self.engine = engine

    def __enter__(self):
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
