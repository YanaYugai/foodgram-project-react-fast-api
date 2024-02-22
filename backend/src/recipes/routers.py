from fastapi import APIRouter
from typing import Annotated, List
from src.recipes.schemas import RecipeCreate, RecipeRead
from fastapi import Header, HTTPException
from src.example_responses import recipes  # noqa: E402

router = APIRouter(prefix="/api/recipes", tags=["recipes"])


tokencorrect = 'TOKENVALUE'


@router.post('/', response_model=RecipeRead, status_code=201)
def create_recipe(
    recipe: RecipeCreate,
    Authorization: Annotated[str, Header()],
):
    if Authorization != f'Token {tokencorrect}':
        raise HTTPException(
            status_code=401,
            detail="Учетные данные не были предоставлены.",
        )
    
    return recipes.get(1)


@router.get('/{recipe_id}/', response_model=RecipeRead)
def get_recipe(recipe_id: int):
    if recipe_id not in recipes:
        raise HTTPException(status_code=404, detail='Страница не найдена.')
    return recipes.get(recipe_id)


@router.get('/', response_model=List[RecipeRead])
def get_recipes():
    return list(recipes.values())


@router.patch('/{recipe_id}/', response_model=RecipeRead)
def patch_recipe(
    recipe_id: int,
    recipe: RecipeCreate,
    Authorization: Annotated[str, Header()],
):
    if Authorization != f'Token {tokencorrect}':
        raise HTTPException(
            status_code=401,
            detail="Учетные данные не были предоставлены.",
        )
    if recipe_id not in recipes:
        raise HTTPException(status_code=404, detail="Страница не найдена.")
    return recipes.get(recipe_id)


@router.delete('/{recipe_id}/', status_code=204)
def delete_recipe(recipe_id: int, Authorization: Annotated[str, Header()]):
    if Authorization != f'Token {tokencorrect}':
        raise HTTPException(
            status_code=401,
            detail="Учетные данные не были предоставлены.",
        )
    if recipe_id not in recipes:
        raise HTTPException(status_code=404, detail="Страница не найдена.")
