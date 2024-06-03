from typing import List

from fastapi import APIRouter
from fastapi_filter import FilterDepends
from sqlalchemy import select

from database import SessionApi
from src.crud import services
from src.models import Ingredient
from src.recipes.filters import IngredientFilter

from .schemas import IngredientsRead

router = APIRouter(prefix="/api/ingredients", tags=["ingredients"])


@router.get('/{ingredient_id}/', response_model=IngredientsRead)
def get_ingredient(ingredient_id: int, session: SessionApi):
    ingredient = services.get_object_by_id_or_error(
        ingredient_id, session, Ingredient
    )
    return ingredient


@router.get('/', response_model=List[IngredientsRead])
def get_ingredients(
    session: SessionApi,
    ingredient_filter: IngredientFilter = FilterDepends(IngredientFilter),
):
    ingredients = select(Ingredient)
    query = ingredient_filter.filter(ingredients)
    result = session.execute(query)
    return result.scalars().all()
