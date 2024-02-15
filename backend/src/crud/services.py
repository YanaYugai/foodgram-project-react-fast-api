from backend.src.models import User, Recipe
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Header
from http import HTTPStatus
from backend.src.users.schemas import UserTokenCreation, UserCreation
from backend.src.recipes.schemas import RecipeCreate
from pydantic import BaseModel


def get_object_by_id_or_error(id: int, session: Session, model: BaseModel):
    obj = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return obj


def get_objects(session: Session, model: BaseModel):
    statement = select(model)
    objects = session.scalars(statement).all()
    return objects


def create_token_or_error(session: Session, data: UserTokenCreation):
    email = data.get('email')
    password = data.get('password')
    query = select(User).where(User.email == email)
    user = session.scalar(query)
    if user is None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    if user.password != password:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    #return generate_token(user)


def create_user(session: Session, data: UserCreation):
    username = data.username
    statement = select(User).where(User.username == username)
    user = session.scalar(statement)
    if user is not None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    user = User(**data.model_dump())
    session.add(user)
    session.commit()
    return user


def create_recipe(session: Session, data: RecipeCreate):
    recipe = Recipe(data)
    session.add(recipe)
    session.commit()
    return recipe

# def create_post(token: str = Depends(get), Authorization: Annotated[str, Header()]):


def delete_object(
    session: Session,
    id: int,
    model: BaseModel,
):
    obj = get_object_by_id_or_error(id, session, model)
    session.delete(obj)
    session.commit()
    return HTTPStatus.NO_CONTENT
