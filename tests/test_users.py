import http

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.src.crud.services import (
    create_user,
    get_object_by_id_or_error,
    get_objects,
)
from backend.src.models import User
from backend.src.users.schemas import UserCreation


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
    assert response.status_code == http.HTTPStatus.OK


def test_get_users(
    client,
    clear_tables: Session,
) -> None:
    users = get_objects(clear_tables, User)
    count_users = clear_tables.scalar(select(func.count(User.id)))
    assert len(users) == count_users
    response = client.get('/api/users/')
    assert response.status_code == http.HTTPStatus.OK
