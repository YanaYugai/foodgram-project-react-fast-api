from fastapi.testclient import TestClient
from pytest import fixture
from typing import Generator
from sqlalchemy.orm import sessionmaker
from main import app
from database import engine, Base
from sqlalchemy.sql import text


TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@fixture(scope="session")
def session() -> Generator:
    with TestSession() as session:
        yield session


@fixture(scope="function")
def clear_tables(session) -> Generator:
    yield session
    for table in Base.metadata.sorted_tables:
        session.execute(
            text(f'TRUNCATE "{table.name}" RESTART IDENTITY CASCADE;'),
        )
    session.commit()


@fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
