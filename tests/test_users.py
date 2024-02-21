from tests.example_responses import users
import http
from sqlalchemy.orm import Session
from sqlalchemy import func, select
import random
import string
from src.users.schemas import UserCreation
from src.models import User
from src.crud.services import create_user, get_object_by_id_or_error, get_objects


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def test_get_users_response(client):
    raise NotImplementedError


def test_get_profile(client):
    raise NotImplementedError


def test_create_token(client):
    raise NotImplementedError


def test_delete_token(client):
    raise NotImplementedError


def test_change_password(client):
    raise NotImplementedError


def test_get_user_response(client):
    response = client.get('/api/users/1/')
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == users[1]


def test_post_user(client):
    response = client.post(
        '/api/users/',
        json={
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "Qwerty123",
        },
    )
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json() == {
        "email": "vpupkin@yandex.ru",
        "id": 0,
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин",
    }


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    first_name = random_lower_string()
    last_name = random_lower_string()
    user_in = UserCreation(email=email, password=password, username=username, first_name=first_name, last_name=last_name)
    user = create_user(session=db, data=user_in)
    assert user.email == email
    assert user.username == username
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert hasattr(user, "password")


def test_get_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    first_name = random_lower_string()
    last_name = random_lower_string()
    user_in = UserCreation(email=email, password=password, username=username, first_name=first_name, last_name=last_name)
    user = create_user(session=db, data=user_in)
    user_check = get_object_by_id_or_error(user.id, db, User)
    assert user.email == user_check.email
    assert user.username == user_check.username


def test_get_users(db: Session):
    users = get_objects(db, User)
    count_users = db.scalar(select(func.count(User.id)))
    assert len(users) == count_users

