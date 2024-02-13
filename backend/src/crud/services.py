from models import User
from sqlalchemy import select
from sqlalchemy. orm import Session
from fastapi import HTTPException
from users.schemas import UserTokenCreation, UserCreation


def get_object_by_id_or_error(id: int, session: Session, model):
    statement = select(model).where(model.id == id)
    obj = session.scalar(statement)
    if obj is None:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return obj


def get_objects(session: Session, model):
    statement = select(model)
    objects = session.scalars(statement)
    return objects


def get_token_or_error(session: Session, data: UserTokenCreation):
    email = data.get('email')
    password = data.get('password')
    query = select(User).where(User.email == email)
    user = session.scalar(query)
    if user is None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    if user.password != password:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    return generate_token(user)


def create_user(session: Session, data: UserCreation):
    username = data.get('username')
    statement = select(User).where(User.username == username)
    user = session.scalar(statement)
    if user is not None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    user = User(data)
    session.add(user)
    session.commit()
    return user

