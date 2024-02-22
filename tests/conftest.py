from fastapi.testclient import TestClient
from pytest import fixture
from typing import Generator
from sqlalchemy.orm import sessionmaker
from main import app
from database import engine, Base
from contextlib import contextmanager
from sqlalchemy.sql import text


TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def clear_tables():
    with TestSession() as conn:
        for table in Base.metadata.sorted_tables:
            conn.execute(text(f'TRUNCATE "{table.name}" RESTART IDENTITY CASCADE;'))
        conn.commit()


@fixture(scope="session")
def db() -> Generator:
    with TestSession() as session:
        yield session
    clear_tables()


@fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
