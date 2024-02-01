from tests.example_responses import users
import http


def test_get_users(client):
    raise NotImplementedError


def test_get_profile(client):
    raise NotImplementedError


def test_create_token(client):
    raise NotImplementedError


def test_delete_token(client):
    raise NotImplementedError


def test_change_password(client):
    raise NotImplementedError


def test_get_user(client):
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
            "password": "Qwerty123"
        },
    )
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json() == {
        "email": "vpupkin@yandex.ru",
        "id": 0,
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин"
    }
