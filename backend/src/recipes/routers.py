from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from backend.database import SessionApi
from backend.src.auth.utils import (
    oauth2_scheme,
    oauth2_scheme_token_not_necessary,
)
from backend.src.crud import services
from backend.src.models import Cart, Favorite, Recipe
from backend.src.recipes.schemas import (
    RecipeCreate,
    RecipeRead,
    RecipeReadShort,
)

router = APIRouter(prefix="/api/recipes", tags=["recipes"])


tokencorrect = 'TOKENVALUE'


@router.post('/', response_model=RecipeRead, status_code=201)
def create_recipe(
    session: SessionApi,
    recipe_data: RecipeCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(session=session, token=token)
    recipe_data = recipe_data.model_dump()
    ingredients = recipe_data.pop('ingredients')
    tags = recipe_data.pop('tags')
    recipe = Recipe(**recipe_data, author_id=current_user.id)
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    recipe_with_ingredients_and_tags = (
        services.create_ingredients_tags_in_recipe(
            session=session,
            ingredients=ingredients,
            tags=tags,
            recipe=recipe,
        )
    )
    recipe_correct_response = services.get_is_subs_is_favorited_is_sc(
        recipe=recipe_with_ingredients_and_tags,
        session=session,
        current_user=current_user,
    )
    return recipe_correct_response


@router.get('/{recipe_id}/', response_model=RecipeRead)
def get_recipe(
    recipe_id: int,
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme_token_not_necessary)],
):
    recipe = services.get_object_by_id_or_error(
        id=recipe_id,
        session=session,
        model=Recipe,
    )
    current_user = services.get_current_user_without_error(
        session=session,
        token=token,
    )
    recipe = services.get_is_subs_is_favorited_is_sc(
        recipe=recipe,
        session=session,
        current_user=current_user,
    )
    return recipe


@router.get('/', response_model=List[RecipeRead])
def get_recipes(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme_token_not_necessary)],
):
    recipes_new = []
    current_user = services.get_current_user_without_error(
        session=session,
        token=token,
    )
    recipes = services.get_objects(session=session, model=Recipe)
    for recipe in recipes:
        recipe = services.get_is_subs_is_favorited_is_sc(
            recipe=recipe,
            session=session,
            current_user=current_user,
        )
        recipes_new.append(recipe)
    return recipes_new


@router.patch('/{recipe_id}/', response_model=RecipeRead)
def patch_recipe(
    recipe_id: int,
    session: SessionApi,
    recipe_data: RecipeCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(session=session, token=token)
    recipe = services.get_object_by_id_or_error(
        id=recipe_id,
        session=session,
        model=Recipe,
    )
    recipe_data = recipe_data.model_dump()
    ingredients = recipe_data.pop('ingredients')
    tags = recipe_data.pop('tags')
    services.check_user_is_author(user=current_user, recipe=recipe)
    recipe = Recipe(**recipe_data, author_id=current_user.id)
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    recipe_with_ingredients_and_tags = (
        services.create_ingredients_tags_in_recipe(
            session=session,
            ingredients=ingredients,
            tags=tags,
            recipe=recipe,
        )
    )
    recipe_correct_response = services.get_is_subs_is_favorited_is_sc(
        recipe=recipe_with_ingredients_and_tags,
        session=session,
        current_user=current_user,
    )
    return recipe_correct_response


@router.post(
    '/{recipe_id}/favorite/', response_model=RecipeReadShort, status_code=201
)
def add_recipe_to_favorite(
    recipe_id: int,
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(session=session, token=token)
    recipe = services.get_object_by_id_or_error(
        id=recipe_id,
        session=session,
        model=Recipe,
    )
    services.create_favorite_cart(
        id=recipe.id,
        session=session,
        current_user=current_user,
        model=Favorite,
    )
    return recipe


@router.delete('/{recipe_id}/favorite/', status_code=204)
def delete_recipe_from_favorite(
    recipe_id: int,
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(session=session, token=token)
    recipe = services.get_object_by_id_or_error(
        id=recipe_id,
        session=session,
        model=Recipe,
    )
    statement = select(Favorite).where(
        Favorite.recipe_id == recipe.id,
        Favorite.user_id == current_user.id,
    )
    favorite = session.scalar(statement)
    if favorite is None:
        raise HTTPException(status_code=400, detail='Рецепта нет в избранном.')
    session.delete(favorite)
    session.commit()


@router.post(
    '/{recipe_id}/shopping_cart/',
    response_model=RecipeReadShort,
    status_code=201,
)
def add_recipe_to_cart(
    recipe_id: int,
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(session=session, token=token)
    recipe = services.get_object_by_id_or_error(
        id=recipe_id,
        session=session,
        model=Recipe,
    )
    services.create_favorite_cart(
        id=recipe.id,
        session=session,
        current_user=current_user,
        model=Cart,
    )
    return recipe


@router.delete('/{recipe_id}/shopping_cart/', status_code=204)
def delete_recipe_from_cart(
    recipe_id: int,
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(session=session, token=token)
    recipe = services.get_object_by_id_or_error(
        id=recipe_id,
        session=session,
        model=Recipe,
    )
    statement = select(Cart).where(
        Cart.recipe_id == recipe.id,
        Cart.user_id == current_user.id,
    )
    cart = session.scalar(statement)
    if cart is None:
        raise HTTPException(status_code=400, detail='Рецепта нет в корзине.')
    session.delete(cart)
    session.commit()


@router.delete('/{recipe_id}/', status_code=204)
def delete_recipe(
    recipe_id: int,
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(
        session=session,
        token=token,
    )
    recipe = services.get_object_by_id_or_error(
        id=recipe_id,
        session=session,
        model=Recipe,
    )
    services.check_user_is_author(
        user=current_user,
        recipe=recipe,
    )
    services.delete_object_by_id(
        session=session,
        id=recipe.id,
        model=Recipe,
    )
