import dataclasses
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.database import SessionApi
from backend.src.auth.utils import get_password_hash, oauth2_scheme
from backend.src.crud import services
from backend.src.models import User
from backend.src.users.schemas import (
    AuthorRead,
    UserCreation,
    UserPasswordReset,
    UserResponseCreation,
)

router = APIRouter(prefix='/api/users', tags=['users'])


@router.post(
    "/set_password/",
    status_code=204,
)
def set_password(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
    data: UserPasswordReset,
):
    user = services.get_current_user(session=session, token=token)
    user = services.authenticate_user(
        session=session,
        email=user.email,
        password=data.current_password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect field",
        )
    hashed_password = get_password_hash(data.new_password)
    user.password = hashed_password
    session.add(user)
    session.commit()


@router.get('/me/', response_model=UserResponseCreation)
def get_me(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    user = services.get_current_user(session=session, token=token)
    return user


@router.post('/{user_id}/subscribe/', response_model=AuthorRead)
def followed_user(
    user_id: int,
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    user = services.get_object_by_id_or_error(
        id=user_id,
        session=session,
        model=User,
    )
    current_user = services.get_current_user(session=session, token=token)
    subscribtion = services.create_subscribtion(
        session=session,
        id=user.id,
        current_user=current_user,
    )
    following = services.get_object_by_id_or_error(
        id=subscribtion.following_id,
        session=session,
        model=User,
    )
    """
    TODO: try experiment
    return AuthorRead.model_validate(
        obj=following,
        context={"is_subscribed": True},
    )
    """
    return {**dataclasses.asdict(following), 'is_subscribed': True}


@router.get('/{user_id}/', response_model=UserResponseCreation)
def get_user(user_id: int, session: SessionApi):
    user = services.get_object_by_id_or_error(
        id=user_id,
        session=session,
        model=User,
    )
    return user


@router.post('/', response_model=UserResponseCreation, status_code=201)
def post_user(user_data: UserCreation, session: SessionApi):
    user = services.create_user(session, user_data)
    return user


@router.get('/', response_model=List[UserResponseCreation])
def get_users(session: SessionApi):
    users = services.get_objects(session=session, model=User)
    return users
