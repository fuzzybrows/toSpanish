from typing import Annotated

from fastapi import Depends
from sqlalchemy.engine.url import make_url
from sqlalchemy.sql.expression import text
from sqlmodel import Session, SQLModel, create_engine

from app.settings import settings

engine = create_engine(settings.database_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]



def create_database(config, logger) -> None:  # pragma: no cover
    """
    Creates a database if one does not exist.
    This will just fail if the database doesn't exist
    Note: we have to connect to the "postgres" database because the target database doesn't exist yet
    """
    url = make_url(config.get_main_option("sqlalchemy.url"))
    target_database = url.database
    connectable = create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")

    with connectable.connect() as connection:
        result = connection.execute(
            text(f"SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('{target_database}')")
        )
        if result.one_or_none():
            logger.info(f"Database '{target_database}' already exists  - not creating")
            return

        connection.execute(text(f"CREATE DATABASE {target_database}"))
        logger.info(f"Database '{target_database}' created")

