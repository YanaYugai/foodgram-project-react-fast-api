from typing import Annotated, List

from fastapi import APIRouter, Depends, Header, HTTPException

from backend.database import SessionApi
from backend.src.auth.utils import oauth2_scheme
from backend.src.crud import services
from backend.src.example_responses import recipes  # noqa: E402
from backend.src.models import Recipe
from backend.src.recipes.schemas import RecipeCreate, RecipeRead

router = APIRouter(prefix="/api/recipes", tags=["recipes"])


tokencorrect = 'TOKENVALUE'


@router.post('/', response_model=RecipeRead, status_code=201)
def create_recipe(
    session: SessionApi,
    recipe_data: RecipeCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(session=session, token=token)
    recipe = Recipe(**recipe_data.model_dump(), author_id=current_user.id)
    session.add(recipe)
    session.commit()
    return recipe


@router.get('/{recipe_id}/', response_model=RecipeRead)
def get_recipe(recipe_id: int, session: SessionApi):
    recipe = services.get_object_by_id_or_error(
        id=recipe_id,
        session=session,
        model=Recipe,
    )
    return recipe


@router.get('/', response_model=List[RecipeRead])
def get_recipes(session: SessionApi):
    recipes = services.get_objects(session=session, model=Recipe)
    return recipes


@router.patch('/{recipe_id}/', response_model=RecipeRead)
def patch_recipe(
    recipe_id: int,
    session: SessionApi,
    recipe_data: RecipeCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    current_user = services.get_current_user(session=session, token=token)
    recipe = services.get_object_by_id_or_error(
        id=recipe_id, session=session, model=Recipe
    )
    if recipe.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="У вас недостаточно прав для выполнения данного действия.",
        )
    recipe = Recipe(**recipe_data.model_dump(), author_id=current_user.id)
    session.add(recipe)
    session.commit()
    return recipe


@router.delete('/{recipe_id}/', status_code=204)
def delete_recipe(recipe_id: int, Authorization: Annotated[str, Header()]):
    if Authorization != f'Token {tokencorrect}':
        raise HTTPException(
            status_code=401,
            detail="Учетные данные не были предоставлены.",
        )
    if recipe_id not in recipes:
        raise HTTPException(status_code=404, detail="Страница не найдена.")
