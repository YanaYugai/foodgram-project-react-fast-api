from http import HTTPStatus
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.src.auth.utils import (
    ALGORITHM,
    SECRET_KEY,
    get_password_hash,
    verify_password,
)
from backend.src.models import User  # type: ignore
from backend.src.users.schemas import UserCreation
from database import Base


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
    hashed_password = get_password_hash(data.password)
    data_new = data.model_copy()
    data_new.password = hashed_password
    user = User(**data_new.model_dump())
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
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
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
