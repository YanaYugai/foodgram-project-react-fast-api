from fastapi import APIRouter
from typing import List
import path
import sys
from fastapi import Header, HTTPException
from backend.src.ingredients.schemas import IngredientsRead


directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent.parent.parent)

from tests.example_responses import ingredients  # noqa: E402


router = APIRouter(prefix="/api/ingredients", tags=["ingredients"])


@router.get('/{ingredient_id}/', response_model=IngredientsRead)
def get_ingredient(ingredient_id: int):
    if ingredient_id not in ingredients:
        raise HTTPException(
            status_code=404, detail="Страница не найдена.",
        )
    return ingredients.get(ingredient_id)


@router.get('/', response_model=List[IngredientsRead])
def get_ingredients():
    return list(ingredients.values())
