from fastapi import APIRouter
from src.users.schemas import (
    UserCreation,
    UserResponseCreation,
)
from database import SessionApi
from src.crud import services
from backend.src.models import User
from typing import List


router = APIRouter(prefix='/api/users', tags=['users'])


@router.get('/{user_id}/', response_model=UserResponseCreation)
def get_user(user_id: int, session: SessionApi):
    user = services.get_object_by_id_or_error(
        id=user_id, session=session, model=User,
    )
    return user


@router.post('/', response_model=UserResponseCreation, status_code=201)
def post_user(user: UserCreation, session: SessionApi):
    user = services.create_user(session, user)
    return user


@router.get('/', response_model=List[UserResponseCreation])
def get_users(session: SessionApi):
    users = services.get_objects(session=session, model=User)
    return users
