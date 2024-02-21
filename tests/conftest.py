from fastapi.testclient import TestClient
from pytest import fixture
from typing import Generator
from sqlalchemy.orm import Session
from main import app
from database import engine


@fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        yield session


@fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
