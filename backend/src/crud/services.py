from http import HTTPStatus
from typing import Any, List

from fastapi import HTTPException
from sqlalchemy import select

from backend.src.models import Recipe, User
from database import Base, SessionApi
from src.recipes.schemas import RecipeCreate
from src.users.schemas import UserCreation, UserTokenCreation


def get_object_by_id_or_error(
    id: int,
    session: SessionApi,
    model: Base,
) -> Any:
    obj = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return obj


def get_objects(session: SessionApi, model: Base) -> List[Base]:
    statement = select(model)
    objects = session.scalars(statement).all()
    return objects


def get_user_by_email(session: SessionApi, data: UserTokenCreation) -> Any:
    email = data.get('email')
    password = data.get('password')
    statement = select(User).where(
        User.email == email,
        User.password == password,
    )
    user = session.scalar(statement)
    if user is None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    return user


def create_token_or_error(session: SessionApi, data: UserTokenCreation):
    email = data.get('email')
    password = data.get('password')
    query = select(User).where(User.email == email)
    user = session.scalar(query)
    if user is None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    if user.password != password:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    #  return generate_token(user)


def create_user(session: SessionApi, data: UserCreation) -> Any:
    username = data.username
    statement = select(User).where(User.username == username)
    user = session.scalar(statement)
    if user is not None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    user = User(**data.model_dump())
    session.add(user)
    session.commit()
    return user


def create_recipe(session: SessionApi, data: RecipeCreate) -> Recipe:
    recipe = Recipe(data)
    session.add(recipe)
    session.commit()
    return recipe


def delete_object(
    session: SessionApi,
    id: int,
    model: Base,
) -> Any:
    obj = get_object_by_id_or_error(id, session, model)
    session.delete(obj)
    session.commit()
    return HTTPStatus.NO_CONTENT
