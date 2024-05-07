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
from backend.src.recipes.schemas import RecipeCreate
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
        if table.name not in ('ingredient', 'tag'):
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
def recipe_data() -> RecipeCreate:
    image = "data:image/png;base64,\n"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/\n"
    "S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByx\n"
    "OyYQAAAABJRU5ErkJggg=="
    name = random_lower_string()
    text = random_lower_string()
    cooking_time = 100
    tags = [1]
    ingredients = [{"id": 1, "amount": 10}, {"id": 3, "amount": 10}]
    recipe_in = RecipeCreate(
        image=image,
        name=name,
        text=text,
        cooking_time=cooking_time,
        tags=tags,
        ingredients=ingredients,
    )
    return recipe_in


def recipe_data_function() -> RecipeCreate:
    image = "data:image/png;base64,\n"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/\n"
    "S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByx\n"
    "OyYQAAAABJRU5ErkJggg=="
    name = random_lower_string()
    text = random_lower_string()
    cooking_time = 100
    tags = [2]
    ingredients = [
        {"id": 1, "amount": 10},
        {"id": 10, "amount": 10},
        {"id": 11, "amount": 10},
    ]
    recipe_in = RecipeCreate(
        image=image,
        name=name,
        text=text,
        cooking_time=cooking_time,
        tags=tags,
        ingredients=ingredients,
    )
    return recipe_in


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


@fixture(scope="function")
def following_with_5_recipes(
    client,
    headers: dict[str, str],
    clear_tables: Session,
    user_data: UserCreation,
):
    user = services.create_user(session=clear_tables, data=user_data)
    login_data = {
        "username": user.email,
        "password": user_data.password,
    }
    response = client.post('api/token/login/', data=login_data)
    tokens = response.json()
    token = tokens["access_token"]
    headers_user = {"Authorization": f"Token {token}"}
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        f'/api/users/{user.id}/subscribe/',
        headers=headers,
    )
    return user.id, headers


@fixture(scope="function")
def cart_with_5_recipes(
    client,
    headers: dict[str, str],
    clear_tables: Session,
    user_data: UserCreation,
):
    user = services.create_user(session=clear_tables, data=user_data)
    login_data = {
        "username": user.email,
        "password": user_data.password,
    }
    response = client.post('api/token/login/', data=login_data)
    tokens = response.json()
    token = tokens["access_token"]
    headers_user = {"Authorization": f"Token {token}"}
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        url="/api/recipes/",
        headers=headers_user,
        json=recipe_data_function().model_dump(),
    )
    client.post(
        '/api/recipes/1/shopping_cart/',
        headers=headers,
    )
    client.post(
        '/api/recipes/2/shopping_cart/',
        headers=headers,
    )
    client.post(
        '/api/recipes/3/shopping_cart/',
        headers=headers,
    )
    client.post(
        '/api/recipes/4/shopping_cart/',
        headers=headers,
    )
    client.post(
        '/api/recipes/5/shopping_cart/',
        headers=headers,
    )
    return headers


@fixture(scope="function")
def recipe(
    client,
    headers: dict[str, str],
    recipe_data: RecipeCreate,
):
    response = client.post(
        url="/api/recipes/",
        headers=headers,
        json=recipe_data.model_dump(),
    )
    recipe = response.json()
    return recipe, headers
