from collections.abc import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT current_database(), current_schema()"))

        return {
            "database": "connected",
            "message": "Database connection successful"
        }

    except SQLAlchemyError as e:
        return {
            "database": "not connected",
            "error": str(e)
        }