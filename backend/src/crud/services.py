import base64
import os
import random
import string
from http import HTTPStatus
from typing import Any, Optional, Sequence, Union

from fastapi import HTTPException, status
from fpdf import FPDF
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.selectable import Select

from src.auth.utils import (
    ALGORITHM,
    SECRET_KEY,
    get_password_hash,
    verify_password,
)
from src.models import (
    Cart,
    Favorite,
    Follow,
    IngredientsInRecipe,
    Recipe,
    TagsInRecipe,
    User,
)
from src.users.schemas import UserCreation


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=8))


def get_object_by_id_or_error(id: int, session: Session, model: Any):
    obj = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return obj


def get_objects(session: Session, model: Any) -> Sequence[Any]:
    statement = select(model)
    objects = session.scalars(statement).all()
    return objects


def create_user(session: Session, data: UserCreation) -> User:
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


def create_subscribtion(
    session: Session,
    id: int,
    current_user: User,
) -> Follow:
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
    session.commit()
    return subscribtion


def check_is_subscribed(
    session: Session,
    id: int,
    current_user_id: int,
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


def check_is_favorite_cart(
    session: Session,
    id: int,
    current_user_id: int,
    model: Any,
) -> bool:
    is_cart_favorite = False
    statement = select(model).where(
        model.user_id == current_user_id,
        model.recipe_id == id,
    )
    favorite_cart = session.scalar(statement)
    if favorite_cart is not None:
        is_cart_favorite = True
    return is_cart_favorite


def filter_cart_favorite(
    current_user: User,
    queryset: Union[Query, Select],
    is_in_shopping_cart: Optional[int],
    is_favorited: Optional[int],
) -> Union[Query, Select]:
    if current_user is not None:
        if is_in_shopping_cart:
            queryset = queryset.filter(Cart.user_id == current_user.id)
        if is_favorited:
            queryset = queryset.filter(Favorite.user_id == current_user.id)
    return queryset


def download_shopping_list(ingredients: list[Any]):
    ing_list = [f'{ing[1]} ' f'({ing[2]}) - {ing[0]}' for ing in ingredients]
    pdf = FPDF()
    pdf.add_font(
        'DejaVu',
        style="",
        fname="../data/DejaVuSansCondensed.ttf",
        uni=True,
    )
    pdf.add_page()
    pdf.set_font('DejaVu', '', 14)
    for ingredient in ing_list:
        pdf.write(8, ingredient)
        pdf.ln(8)
    return pdf.output(dest='S').encode('utf-8')


def formate_image(image: str) -> str:
    format, imgstr = image.split(';base64,')
    ext = format.split('/')[-1]
    data = base64.b64decode(imgstr)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dirname = os.path.join(BASE_DIR, 'static/job')
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    picture_path = os.path.join(dirname, f'{random_lower_string()}.' + ext)
    with open(picture_path, "wb") as f:
        f.write(data)
    return picture_path


def create_ingredients_tags_in_recipe(
    session: Session,
    ingredients: list[dict[str, int]],
    tags: list[int],
    recipe: Recipe,
) -> Recipe:
    for ingredient in ingredients:
        ingredient_recipe = IngredientsInRecipe(
            recipe_id=recipe.id,
            ingredient_id=ingredient['id'],
            amount=ingredient['amount'],
        )
        recipe.ingredients.append(ingredient_recipe)
    for tag in tags:
        session.add(
            TagsInRecipe(
                recipe_id=recipe.id,
                tag_id=tag,
            ),
        )
    session.commit()
    session.refresh(recipe)
    return recipe


def get_is_subscribed(
    session: Session,
    current_user: Optional[User],
    user: User,
) -> User:
    if current_user is None:
        is_subscribed = False
    else:
        is_subscribed = check_is_subscribed(
            session=session,
            id=user.id,
            current_user_id=current_user.id,
        )
    user.is_subscribed = is_subscribed
    return user


def get_is_subscribed_count_recipe(
    session: Session,
    current_user: User,
    user: User,
    recipes_limit: Optional[int],
):
    is_subscribed = check_is_subscribed(
        session=session,
        id=user.id,
        current_user_id=current_user.id,
    )
    user.is_subscribed = is_subscribed
    recipes = user.recipes
    recipes_count = len(recipes)
    user.recipes_count = recipes_count
    if recipes_limit is not None:
        try:
            recipes = recipes[:recipes_limit]
            user.recipes = recipes
        except ValueError:
            raise HTTPException(status_code=400, detail="Неверное значение.")
    return user


def get_is_subs_is_favorited_is_sc(
    recipe: Recipe,
    session: Session,
    current_user: Optional[User],
) -> Recipe:
    author = recipe.author
    if current_user is None:
        is_subscribed = False
        is_favorited = False
        is_in_shopping_cart = False
    else:
        is_subscribed = check_is_subscribed(
            session,
            id=author.id,
            current_user_id=current_user.id,
        )
        is_favorited = check_is_favorite_cart(
            session=session,
            id=recipe.id,
            current_user_id=current_user.id,
            model=Favorite,
        )
        is_in_shopping_cart = check_is_favorite_cart(
            session=session,
            id=recipe.id,
            current_user_id=current_user.id,
            model=Cart,
        )
    author.is_subscribed = is_subscribed
    recipe.author = author
    recipe.is_favorited = is_favorited
    recipe.is_in_shopping_cart = is_in_shopping_cart
    return recipe


def create_favorite_cart(
    session: Session,
    id: int,
    current_user: User,
    model: Any,
) -> Any:
    statement = select(model).where(
        model.user_id == current_user.id,
        model.recipe_id == id,
    )
    favorite_cart = session.scalar(statement)
    if favorite_cart is not None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')
    favorite_cart = model(user_id=current_user.id, recipe_id=id)
    session.add(favorite_cart)
    session.commit()
    return favorite_cart


def get_subscribtion_or_error(
    session: Session,
    id: int,
    current_user_id: int,
) -> Follow:
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


def delete_object_by_id(
    session: Session,
    id: int,
    model: Any,
) -> Any:
    obj = get_object_by_id_or_error(id, session, model)
    session.delete(obj)
    session.commit()
    return HTTPStatus.NO_CONTENT


def authenticate_user(
    session: Session,
    email: str,
    password: str,
) -> User:
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
) -> User:
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


def check_user_is_author(
    user: User,
    recipe: Recipe,
) -> None:
    if user.id != recipe.author_id:
        raise HTTPException(
            status_code=403,
            detail="У вас недостаточно прав для выполнения данного действия.",
        )


def get_current_user_without_error(
    session: Session,
    token: str,
) -> User:
    try:
        current_user = get_current_user(session=session, token=token)
    except AttributeError:
        current_user = None
    return current_user
