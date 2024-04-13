from typing import List

from fastapi import APIRouter

from backend.database import SessionApi
from backend.src.crud import services
from backend.src.ingredients.schemas import IngredientsRead
from backend.src.models import Ingredient

router = APIRouter(prefix="/api/ingredients", tags=["ingredients"])


@router.get('/{ingredient_id}/', response_model=IngredientsRead)
def get_ingredient(ingredient_id: int, session: SessionApi):
    ingredient = services.get_object_by_id_or_error(
        ingredient_id, session, Ingredient
    )
    return ingredient


@router.get('/', response_model=List[IngredientsRead])
def get_ingredients(session: SessionApi):
    ingredients = services.get_objects(session, Ingredient)
    return ingredients
