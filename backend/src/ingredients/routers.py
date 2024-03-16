from typing import List

from fastapi import APIRouter, HTTPException

from backend.src.example_responses import ingredients  # noqa: E402
from backend.src.ingredients.schemas import IngredientsRead

router = APIRouter(prefix="/api/ingredients", tags=["ingredients"])


@router.get('/{ingredient_id}/', response_model=IngredientsRead)
def get_ingredient(ingredient_id: int):
    if ingredient_id not in ingredients:
        raise HTTPException(
            status_code=404,
            detail="Страница не найдена.",
        )
    return ingredients.get(ingredient_id)


@router.get('/', response_model=List[IngredientsRead])
def get_ingredients():
    return list(ingredients.values())
