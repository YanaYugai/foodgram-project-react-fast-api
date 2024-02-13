from models import User
from sqlalchemy import select
from sqlalchemy. orm import Session
from fastapi import HTTPException
from users.schemas import UserTokenCreation


def get_user_by_id_or_error(id: int, session: Session):
    query = select(User).where(User.id == id)
    user = session.scalar(query)
    if user is None:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return user


def get_users(session: Session):
    statement = select(User)
    users = session.scalars(statement)
    return users


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


