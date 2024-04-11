import random
import string
from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text

from backend.database import engine
from backend.main import app
from backend.src.crud import services
from backend.src.models import Base
from backend.src.users.schemas import UserCreation

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


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


@fixture(scope="function")
def user_data() -> UserCreation:
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    first_name = random_lower_string()
    last_name = random_lower_string()
    user_in = UserCreation(
        email=email,
        password=password,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    return user_in


@fixture(scope="function")
def token(
    client,
) -> str:
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    first_name = random_lower_string()
    last_name = random_lower_string()
    user_data = UserCreation(
        email=email,
        password=password,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    user_in = {
        "email": user_data.email,
        "password": user_data.password,
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
    }
    response = client.post('api/users/', json=user_in)
    user = response.json()
    login_data = {
        "username": user['email'],
        "password": user_in["password"],
    }
    response = client.post('api/token/login/', data=login_data)
    tokens = response.json()
    token = tokens["access_token"]
    return token


@fixture(scope="function")
def headers(
    token: str,
) -> dict[str, str]:
    headers = {"Authorization": f"Token {token}"}
    return headers


@fixture(scope="function")
def following(
    client,
    headers: dict[str, str],
    clear_tables: Session,
    user_data: UserCreation,
):
    user = services.create_user(session=clear_tables, data=user_data)
    client.post(
        f'/api/users/{user.id}/subscribe/',
        headers=headers,
    )
    return user.id, headers
