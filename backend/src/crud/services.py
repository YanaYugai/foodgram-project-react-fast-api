from http import HTTPStatus
from typing import Any, Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from psycopg2.errors import UniqueViolation
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.database import Base
from backend.src.auth.utils import (
    ALGORITHM,
    SECRET_KEY,
    get_password_hash,
    verify_password,
)
from backend.src.models import Follow, User  # type: ignore
from backend.src.users.schemas import UserCreation


def get_object_by_id_or_error(id: int, session: Session, model: Any):
    obj = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return obj


def get_objects(session: Session, model: Any):
    statement = select(model)
    objects = session.scalars(statement).all()
    return objects


def create_user(session: Session, data: UserCreation):
    username = data.username
    statement = select(User).where(User.username == username)
    user = session.scalar(statement)
    if user is not None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    hashed_password = get_password_hash(data.password)
    data_new = data.model_copy()
    data_new.password = hashed_password
    user = User(**data_new.model_dump())
    session.add(user)
    session.commit()
    return user


def create_subscribtion(session: Session, id: int, current_user: User):
    if current_user.id == id:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    statement = select(Follow).where(
        Follow.id == current_user.id,
        Follow.following_id == id,
    )
    subscribtion = session.scalar(statement)
    if subscribtion is not None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    subscribtion = Follow(user_id=current_user.id, following_id=id)
    session.add(subscribtion)
    try:
        session.commit()
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        raise HTTPException(status_code=400, detail="Некорректные данные.")
    return subscribtion


def get_subscribtion_or_error(session: Session, id: int, current_user_id: int):
    statement = select(Follow).where(
        Follow.id == current_user_id,
        Follow.following_id == id,
    )
    subscribtion = session.scalar(statement)
    if subscribtion is None:
        raise HTTPException(
            status_code=400,
            detail='Пользователь не подписан.',
        )
    return subscribtion


def check_is_subscribed(
    session: Session, id: int, current_user_id: int
) -> bool:
    is_subscribed = False
    statement = select(Follow).where(
        Follow.id == current_user_id,
        Follow.following_id == id,
    )
    subscribtion = session.scalar(statement)
    if subscribtion is not None:
        is_subscribed = True
    return is_subscribed


def delete_object_by_id(
    session: Session,
    id: int,
    model: Base,
) -> Any:
    obj = get_object_by_id_or_error(id, session, model)
    session.delete(obj)
    session.commit()
    return HTTPStatus.NO_CONTENT


def authenticate_user(session: Session, email: str, password: str):
    statement = select(User).where(
        User.email == email,
    )
    user = session.scalar(statement)
    if user is None:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_current_user(
    session: Session,
    token: str,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Учетные данные не были предоставлены.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_object_by_id_or_error(
        id=int(user_id),
        session=session,
        model=User,
    )
    return user


def get_current_user_without_error(
    session: Session,
    token: str,
):
    try:
        current_user = get_current_user(session=session, token=token)
    except AttributeError:
        current_user = None
    return current_user
