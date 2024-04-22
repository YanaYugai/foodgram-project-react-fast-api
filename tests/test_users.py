import http

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.src.auth.utils import verify_password
from backend.src.crud.services import (
    authenticate_user,
    create_user,
    get_current_user,
    get_object_by_id_or_error,
    get_objects,
)
from backend.src.models import User
from backend.src.users.schemas import UserCreation


def test_get_profile(
    client,
    token: str,
    clear_tables: Session,
) -> None:
    headers = {"Authorization": f"Token {token}"}
    response = client.get('/api/users/me/', headers=headers)
    response_user = response.json()
    user = get_current_user(session=clear_tables, token=token)
    assert response.status_code == 200
    assert user.email == response_user["email"]
    assert user.username == response_user["username"]
    assert user.first_name == response_user["first_name"]
    assert user.last_name == response_user["last_name"]


def test_get_profile_incorrect_token(
    client,
) -> None:
    token = 'Invalid_token'
    headers = {"Authorization": f"Token {token}"}
    response = client.get('/api/users/me/', headers=headers)
    assert response.status_code == 401


def test_authenticate_user(
    clear_tables: Session,
    user_data: UserCreation,
) -> None:
    user = create_user(session=clear_tables, data=user_data)
    authenticated_user = authenticate_user(
        session=clear_tables,
        email=user.email,
        password=user_data.password,
    )
    assert authenticated_user


def test_authenticate_user_invalid_password(
    clear_tables: Session,
    user_data: UserCreation,
) -> None:
    user = create_user(session=clear_tables, data=user_data)
    authenticated_user = authenticate_user(
        session=clear_tables,
        email=user.email,
        password='invalid_password',
    )
    assert not authenticated_user


def test_authenticate_user_invalid_email(
    clear_tables: Session,
    user_data: UserCreation,
) -> None:
    create_user(session=clear_tables, data=user_data)
    authenticated_user = authenticate_user(
        session=clear_tables,
        email='invalid_email',
        password=user_data.password,
    )
    assert not authenticated_user


def test_get_access_token(
    client,
    clear_tables: Session,
    user_data: UserCreation,
) -> None:
    user = create_user(session=clear_tables, data=user_data)
    login_data = {
        "username": user.email,
        "password": user_data.password,
    }
    response = client.post('api/token/login/', data=login_data)
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert "auth_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password(
    client,
    clear_tables: Session,
    user_data: UserCreation,
) -> None:
    user = create_user(session=clear_tables, data=user_data)
    login_data = {
        "username": user.email,
        "password": "invalid_password",
    }
    response = client.post('api/token/login/', data=login_data)
    assert response.status_code == 401


def test_delete_token(client, headers: dict[str, str]):
    response = client.delete('api/token/logout/', headers=headers)
    assert response.status_code == 204


def test_delete_invalid_token(client):
    token = 'invalid_token'
    headers = {"Authorization": f"Token {token}"}
    response = client.delete('api/token/logout/', headers=headers)
    assert response.status_code == 401


def test_change_password(
    client,
    clear_tables: Session,
    user_data: UserCreation,
) -> None:
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
    data = {
        "new_password": "asfakfas",
        "current_password": user_in["password"],
    }
    headers = {"Authorization": f"Token {token}"}
    response = client.post(
        '/api/users/set_password/',
        headers=headers,
        json=data,
    )
    user = get_current_user(
        session=clear_tables,  # type: ignore
        token=tokens["access_token"],
    )
    assert response.status_code == http.HTTPStatus.NO_CONTENT
    assert verify_password("asfakfas", user.password)


def test_create_user(
    clear_tables: Session,
    user_data: UserCreation,
) -> None:
    user = create_user(session=clear_tables, data=user_data)
    assert user.email == user_data.email
    assert user.username == user_data.username
    assert user.first_name == user_data.first_name
    assert user.last_name == user_data.last_name
    assert hasattr(user, "password")


def test_post_user_router(
    client,
    user_data: UserCreation,
) -> None:
    user_in = {
        "email": user_data.email,
        "password": user_data.password,
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
    }
    response = client.post('api/users/', json=user_in)
    user = response.json()
    assert response.status_code == 201
    assert user["email"] == user_data.email
    assert user["username"] == user_data.username
    assert user["first_name"] == user_data.first_name
    assert user["last_name"] == user_data.last_name


def test_get_user(
    client,
    clear_tables: Session,
    user_data: UserCreation,
) -> None:
    user = create_user(session=clear_tables, data=user_data)
    user_check = get_object_by_id_or_error(user.id, clear_tables, User)
    assert user.email == user_check.email
    assert user.username == user_check.username
    response = client.get(f'/api/users/{user.id}/')
    user_response = response.json()
    assert response.status_code == http.HTTPStatus.OK
    assert user_response['is_subscribed'] is False


def test_get_users(
    client,
    clear_tables: Session,
    user_data: UserCreation,
) -> None:
    create_user(session=clear_tables, data=user_data)
    users = get_objects(clear_tables, User)
    count_users = clear_tables.scalar(select(func.count(User.id)))
    assert len(users) == count_users
    response = client.get('/api/users/')
    assert response.status_code == http.HTTPStatus.OK
