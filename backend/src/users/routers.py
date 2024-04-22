from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_paginate import paginate
from sqlalchemy import select

from backend.database import SessionApi
from backend.src.auth.utils import (
    get_password_hash,
    oauth2_scheme,
    oauth2_scheme_token_not_necessary,
)
from backend.src.crud import services
from backend.src.models import Follow, User
from backend.src.recipes.paginator import Page
from backend.src.users.schemas import (
    AuthorRead,
    UserCreation,
    UserPasswordReset,
    UserRead,
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
    return user


@router.post(
    '/{user_id}/subscribe/',
    response_model=UserRead,
    status_code=201,
)
def followed_user(
    user_id: int,
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
    recipes_limit: Union[int, None] = 3,
):
    user = services.get_object_by_id_or_error(
        id=user_id,
        session=session,
        model=User,
    )
    current_user = services.get_current_user(session=session, token=token)
    services.create_subscribtion(
        session=session,
        id=user.id,
        current_user=current_user,
    )
    user = services.get_is_subscribed_count_recipe(
        session=session,
        current_user=current_user,
        user=user,
        recipes_limit=recipes_limit,
    )
    return user


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


@router.get('/subscriptions/')
def get_subscription(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
    recipes_limit: Union[int, None] = 3,
) -> Page[UserRead]:
    current_user = services.get_current_user(session=session, token=token)
    users_is_subscribed = []
    following = current_user.following
    for user in following:
        user = services.get_is_subscribed_count_recipe(
            session, current_user, user, recipes_limit
        )
        users_is_subscribed.append(user)
    return paginate(users_is_subscribed)


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
    user = services.get_is_subscribed(session, current_user, user)
    return user


@router.post('/', response_model=UserResponseCreation, status_code=201)
def post_user(user_data: UserCreation, session: SessionApi):
    user = services.create_user(session, user_data)
    return user


@router.get('/')
def get_users(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme_token_not_necessary)],
) -> Page[AuthorRead]:
    users = services.get_objects(session=session, model=User)
    users_is_subscribed = []
    current_user = services.get_current_user_without_error(
        session=session,
        token=token,
    )
    for user in users:
        user = services.get_is_subscribed(session, current_user, user)
        users_is_subscribed.append(user)
    return paginate(users_is_subscribed)
