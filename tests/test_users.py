from tests.test_recipes import client
from tests.utils import test_nonexistent_objects
from tests.example_responses import users, users_create


test_nonexistent_objects('/api/users/100/', client)


def test_get_users():
    raise NotImplementedError


def test_get_profile():
    raise NotImplementedError


def test_create_token():
    raise NotImplementedError


def test_delete_token():
    raise NotImplementedError


def test_change_password():
    raise NotImplementedError


def test_get_user():
    response = client.get('/api/users/1/')
    assert response.status_code == 200
    assert response.json == users[1]


def test_post_user():
    response = client.post(
        '/api/users/',
        json={
            "email": "dpupkin@yandex.ru",
            "username": "dima.pupkin",
            "first_name": "Дима",
            "last_name": "Пупкин",
            "password": "Qwerty123"
        },
    )
    last_value = list(users_create.values())[-1]
    assert response.status_code == 201
    assert response.json == users_create[last_value]
