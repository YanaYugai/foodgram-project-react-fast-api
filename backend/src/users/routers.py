from fastapi import APIRouter, HTTPException
from src.users.schemas import (
    AuthorRead,
    UserCreation,
    UserResponseCreation,
)
from src.example_responses import users  # noqa: E402


router = APIRouter(prefix='/api/users', tags=['users'])


@router.get('/{user_id}/', response_model=AuthorRead)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return users.get(user_id)


@router.post('/', response_model=UserResponseCreation, status_code=201)
def post_user(user: UserCreation):
    return UserResponseCreation.model_validate(
        {
            "email": "vpupkin@yandex.ru",
            "id": 0,
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
        },
    )
