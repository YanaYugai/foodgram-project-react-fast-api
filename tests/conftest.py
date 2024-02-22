from fastapi.testclient import TestClient
from pytest import fixture
from typing import Generator
from sqlalchemy.orm import sessionmaker
from main import app
from database import engine

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@fixture(scope="session")
def db() -> Generator:
    with TestSession() as session:
        yield session


@fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
