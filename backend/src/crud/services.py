from http import HTTPStatus
from typing import Annotated, Any

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.src.models import Token, User  # type: ignore
from database import Base
from src.auth.routers import oauth2_scheme
from src.users.schemas import UserCreation


def get_object_by_id_or_error(id: int, session: Session, model: Base):
    obj = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return obj


def get_object_by_email_or_error(email: str, password: str, session: Session):
    statement = select(User).where(
        User.email == email,
        User.password == password,
    )
    user = session.scalar(statement)
    if user is None:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return user


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


def delete_object_by_id(
    session: Session,
    id: int,
    model: Base,
) -> Any:
    obj = get_object_by_id_or_error(id, session, model)
    session.delete(obj)
    session.commit()
    return HTTPStatus.NO_CONTENT


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe",
    )


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


def delete_token(
    session: Session,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    statement = select(Token).where(Token.access_token == token)
    token = session.scalar(statement)
    session.delete(token)
    session.commit()
    return HTTPStatus.NO_CONTENT
