import dataclasses
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from backend.database import SessionApi
from backend.src.auth.utils import (
    get_password_hash,
    oauth2_scheme,
    oauth2_scheme_token_not_necessary,
)
from backend.src.crud import services
from backend.src.models import Follow, User
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
    session.commit()


@router.get('/me/', response_model=AuthorRead)
def get_me(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    user = services.get_current_user(session=session, token=token)
    return {**dataclasses.asdict(user), 'is_subscribed': False}


@router.post(
    '/{user_id}/subscribe/',
    response_model=AuthorRead,
    status_code=201,
)
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
    is_subscribed = services.check_is_subscribed(
        session=session,
        id=user.id,
        current_user_id=current_user.id,
    )
    return {**dataclasses.asdict(following), 'is_subscribed': is_subscribed}


@router.delete(
    '/{user_id}/subscribe/',
    status_code=204,
)
def unfollowed_user(
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
    statement = select(Follow).where(
        Follow.id == current_user.id,
        Follow.following_id == user.id,
    )
    subscribtion = session.scalar(statement)
    if subscribtion is None:
        raise HTTPException(
            status_code=400,
            detail='Пользователь не подписан.',
        )
    session.delete(subscribtion)
    session.commit()


@router.get('/subscriptions/', response_model=list[AuthorRead])
def get_subscription(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(session=session, token=token)
    users_is_subscribed = []
    following = current_user.following
    for user in following:
        is_subscribed = services.check_is_subscribed(
            session=session,
            id=user.id,
            current_user_id=current_user.id,
        )
        users_is_subscribed.append(
            {**dataclasses.asdict(user), 'is_subscribed': is_subscribed},
        )
    return users_is_subscribed


@router.get('/{user_id}/', response_model=AuthorRead)
def get_user(
    user_id: int,
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme_token_not_necessary)],
):
    user = services.get_object_by_id_or_error(
        id=user_id,
        session=session,
        model=User,
    )
    current_user = services.get_current_user_without_error(
        session=session,
        token=token,
    )
    if current_user is None:
        is_subscribed = False
    else:
        is_subscribed = services.check_is_subscribed(
            session=session,
            id=user.id,
            current_user_id=current_user.id,
        )
    return {**dataclasses.asdict(user), 'is_subscribed': is_subscribed}


@router.post('/', response_model=UserResponseCreation, status_code=201)
def post_user(user_data: UserCreation, session: SessionApi):
    user = services.create_user(session, user_data)
    return user


@router.get('/', response_model=list[AuthorRead])
def get_users(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme_token_not_necessary)],
):
    users = services.get_objects(session=session, model=User)
    users_is_subscribed = []
    current_user = services.get_current_user_without_error(
        session=session,
        token=token,
    )
    if current_user is None:
        for user in users:
            users_is_subscribed.append(
                {**dataclasses.asdict(user), 'is_subscribed': False},
            )
    else:
        for user in users:
            is_subscribed = services.check_is_subscribed(
                session=session,
                id=user.id,
                current_user_id=current_user.id,
            )
            users_is_subscribed.append(
                {**dataclasses.asdict(user), 'is_subscribed': is_subscribed},
            )
    return users_is_subscribed
