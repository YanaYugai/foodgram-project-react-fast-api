from http import HTTPStatus
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.src.models import User
from database import Base
from src.users.schemas import UserCreation


def get_object_by_id_or_error(id: int, session: Session, model: Base):
    obj = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return obj


def get_objects(session: Session, model: Base):
    statement = select(model)
    objects = session.scalars(statement).all()
    return objects


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


def delete_object(
    session: Session,
    id: int,
    model: Base,
) -> Any:
    obj = get_object_by_id_or_error(id, session, model)
    session.delete(obj)
    session.commit()
    return HTTPStatus.NO_CONTENT
